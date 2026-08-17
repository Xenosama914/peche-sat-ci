"""Les demandes d'inscription venues de la vitrine.

Le formulaire du site public arrive ici. Une demande n'ouvre AUCUN acces : elle se
range dans une table a part, et un humain decide ensuite. C'est la meme honnetete
que le reste du service, cote inscription cette fois.
"""

import datetime

from fastapi import APIRouter, Depends, Header, HTTPException
from sqlalchemy.orm import Session

from app.config import CRON_SECRET
from app.database import get_db
from app.models import DemandeInscription
from app.schemas import DemandeInscriptionIn, DemandeInscriptionOut

router = APIRouter(prefix="/api/inscription", tags=["inscription"])

# Garde-fou anti-inondation : une meme cooperative ne peut pas remplir le formulaire
# cinquante fois d'affilee, volontairement ou par un robot.
FENETRE_ANTI_DOUBLON_MINUTES = 10


@router.post("", response_model=DemandeInscriptionOut, status_code=201)
def creer_demande(payload: DemandeInscriptionIn, db: Session = Depends(get_db)):
    recemment = datetime.datetime.now(datetime.timezone.utc) - datetime.timedelta(
        minutes=FENETRE_ANTI_DOUBLON_MINUTES
    )
    doublon = (
        db.query(DemandeInscription)
        .filter(
            DemandeInscription.cooperative == payload.cooperative.strip(),
            DemandeInscription.contact == payload.contact.strip(),
            DemandeInscription.date_creation >= recemment,
        )
        .first()
    )
    if doublon:
        # On renvoie la demande deja enregistree plutot qu'une erreur : cote visiteur,
        # un double clic ne doit pas ressembler a un echec.
        return doublon

    demande = DemandeInscription(
        cooperative=payload.cooperative.strip(),
        nom_contact=payload.nom_contact.strip(),
        contact=payload.contact.strip(),
        zone=(payload.zone or "").strip() or None,
        nombre_pecheurs=(payload.nombre_pecheurs or "").strip() or None,
        source="vitrine",
    )
    db.add(demande)
    db.commit()
    db.refresh(demande)
    return demande


@router.get("", response_model=list[DemandeInscriptionOut])
def lister_demandes(
    x_admin_secret: str | None = Header(default=None, alias="X-Admin-Secret"),
    db: Session = Depends(get_db),
):
    """Reservee a l'equipe Peche-Sat. Protegee par le meme secret partage que le cron :
    ces demandes contiennent les coordonnees de vraies personnes."""
    if not CRON_SECRET:
        raise HTTPException(status_code=503, detail="Secret d'administration non configure.")
    if x_admin_secret != CRON_SECRET:
        raise HTTPException(status_code=401, detail="Secret d'administration invalide.")

    return (
        db.query(DemandeInscription)
        .order_by(DemandeInscription.date_creation.desc())
        .limit(200)
        .all()
    )
