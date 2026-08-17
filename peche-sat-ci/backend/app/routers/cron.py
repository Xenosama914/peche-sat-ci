"""L'envoi matinal.

Ce que le site promet au pecheur : un mot avant de partir, chaque matin. C'est ici
que cette promesse est tenue.

Le declencheur est EXTERNE (un cron gratuit qui appelle cet endpoint chaque matin),
et non un planificateur interne, pour une raison concrete : les hebergeurs gratuits
mettent l'application en veille apres quelques minutes sans trafic, et un
planificateur endormi n'envoie rien. Un appel entrant, lui, reveille l'application.
"""

import datetime

from fastapi import APIRouter, Depends, Header, HTTPException, Query
from sqlalchemy.orm import Session

from app import zones
from app.config import CRON_SECRET
from app.database import get_db
from app.gee_service import calculer_score
from app.models import Alerte, Pecheur
from app.sms_service import construire_message, envoyer_alerte

router = APIRouter(prefix="/api/cron", tags=["cron"])


def _verifier_secret(secret_recu: str | None) -> None:
    if not CRON_SECRET:
        raise HTTPException(
            status_code=503,
            detail="CRON_SECRET absent de l'environnement : l'envoi matinal est desactive.",
        )
    if secret_recu != CRON_SECRET:
        raise HTTPException(status_code=401, detail="Secret cron invalide.")


def _debut_du_jour() -> datetime.datetime:
    maintenant = datetime.datetime.now(datetime.timezone.utc)
    return maintenant.replace(hour=0, minute=0, second=0, microsecond=0)


@router.post("/envoi-matinal")
def envoi_matinal(
    x_cron_secret: str | None = Header(default=None, alias="X-Cron-Secret"),
    simulation: bool = Query(
        default=False,
        description="Calcule les scores et prepare les messages sans envoyer aucun SMS.",
    ),
    db: Session = Depends(get_db),
):
    """Lit la mer une fois par zone, puis previent chaque pecheur actif de cette zone.

    Le score est calcule UNE SEULE FOIS par zone et non par pecheur : l'appel a
    Google Earth Engine prend plusieurs secondes et est soumis a quota, alors que
    deux pecheurs de la meme zone recoivent forcement la meme lecture.
    """
    _verifier_secret(x_cron_secret)

    pecheurs = db.query(Pecheur).filter(Pecheur.statut == "actif").all()
    if not pecheurs:
        return {
            "statut": "rien a faire",
            "simulation": simulation,
            "pecheurs_actifs": 0,
            "zones": [],
            "envoyes": 0,
            "deja_prevenus": 0,
            "echecs": 0,
        }

    # Qui a deja recu son alerte aujourd'hui : un cron qui se declenche deux fois
    # ne doit jamais faire sonner deux fois le telephone d'un pecheur.
    depuis_minuit = _debut_du_jour()
    deja = {
        ligne[0]
        for ligne in db.query(Alerte.pecheur_id)
        .filter(Alerte.date_envoi >= depuis_minuit, Alerte.statut_sms != "echec")
        .all()
    }

    # Regroupement par zone resolue.
    groupes: dict[str, list[Pecheur]] = {}
    zones_non_reconnues: set[str] = set()
    for pecheur in pecheurs:
        cle, _, _, _, reconnue = zones.resoudre(pecheur.zone_rattachement)
        if not reconnue and pecheur.zone_rattachement:
            zones_non_reconnues.add(pecheur.zone_rattachement)
        groupes.setdefault(cle, []).append(pecheur)

    rapport_zones = []
    total_envoyes = 0
    total_deja = 0
    total_echecs = 0

    for cle, membres in groupes.items():
        _, latitude, longitude, libelle, _ = zones.resoudre(cle)

        # Une zone qui echoue ne doit pas emporter tout l'envoi matinal avec elle.
        try:
            score = calculer_score(latitude, longitude, libelle)
        except Exception as exc:  # noqa: BLE001 - on veut continuer coute que coute
            total_echecs += len(membres)
            rapport_zones.append(
                {
                    "zone": libelle,
                    "pecheurs": len(membres),
                    "statut": "echec lecture satellite",
                    "detail": str(exc)[:200],
                }
            )
            continue

        texte = construire_message(score["decision"], score["zone"], score["message"])
        envoyes_zone = 0
        ignores_zone = 0

        for pecheur in membres:
            if pecheur.id in deja:
                ignores_zone += 1
                total_deja += 1
                continue

            if simulation:
                envoyes_zone += 1
                total_envoyes += 1
                continue

            resultat = envoyer_alerte(pecheur.telephone, texte)
            db.add(
                Alerte(
                    pecheur_id=pecheur.id,
                    cooperative_id=pecheur.cooperative_id,
                    zone=score["zone"],
                    latitude=latitude,
                    longitude=longitude,
                    decision=score["decision"],
                    score=score["score"],
                    chlorophylle_mg_m3=score.get("chlorophylle_mg_m3"),
                    sst_celsius=score.get("sst_celsius"),
                    vent_m_s=score.get("vent_m_s"),
                    statut_sms=resultat["statut"],
                    message=texte,
                )
            )
            envoyes_zone += 1
            total_envoyes += 1

        if not simulation:
            db.commit()

        rapport_zones.append(
            {
                "zone": libelle,
                "pecheurs": len(membres),
                "statut": "ok",
                "decision": score["decision"],
                "score": score["score"],
                "message": texte,
                "envoyes": envoyes_zone,
                "deja_prevenus": ignores_zone,
            }
        )

    return {
        "statut": "termine",
        "simulation": simulation,
        "horodatage": datetime.datetime.now(datetime.timezone.utc).isoformat(),
        "pecheurs_actifs": len(pecheurs),
        "zones": rapport_zones,
        "envoyes": total_envoyes,
        "deja_prevenus": total_deja,
        "echecs": total_echecs,
        "zones_non_reconnues": sorted(zones_non_reconnues),
    }


@router.get("/zones")
def lister_zones():
    """Les zones connues, pour que l'interface propose une liste au lieu d'un champ libre."""
    return zones.liste_zones()
