import datetime

from fastapi import APIRouter, Depends
from sqlalchemy import func
from sqlalchemy.orm import Session

from app.auth import cooperative_actuelle
from app.database import get_db
from app.models import Alerte, Cooperative, Pecheur
from app.schemas import (
    AlertesParJour,
    AlerteJournalOut,
    RepartitionDecision,
    TableauBordCooperativeOut,
)

router = APIRouter(prefix="/api/cooperative", tags=["cooperative"])


@router.get("/tableau-de-bord", response_model=TableauBordCooperativeOut)
def tableau_de_bord(
    cooperative: Cooperative = Depends(cooperative_actuelle),
    db: Session = Depends(get_db),
):
    pecheurs_actifs = (
        db.query(func.count(Pecheur.id))
        .filter(Pecheur.cooperative_id == cooperative.id, Pecheur.statut == "actif")
        .scalar()
    )

    depuis_30j = datetime.datetime.now(datetime.timezone.utc) - datetime.timedelta(days=30)
    alertes_base = db.query(Alerte).filter(
        Alerte.cooperative_id == cooperative.id, Alerte.date_envoi >= depuis_30j
    )
    alertes_30j = alertes_base.count()
    sms_envoyes_30j = alertes_base.filter(Alerte.statut_sms == "envoye").count()
    evitez_30j = alertes_base.filter(Alerte.decision == "EVITEZ").count()
    taux_evitez_pct = round(100 * evitez_30j / alertes_30j, 1) if alertes_30j else 0.0

    repartition_brute = (
        db.query(Alerte.decision, func.count(Alerte.id))
        .filter(Alerte.cooperative_id == cooperative.id, Alerte.date_envoi >= depuis_30j)
        .group_by(Alerte.decision)
        .all()
    )
    repartition_decisions = [
        RepartitionDecision(decision=decision or "INCONNU", total=total) for decision, total in repartition_brute
    ]

    depuis_14j = datetime.datetime.now(datetime.timezone.utc) - datetime.timedelta(days=14)
    lignes_14j = (
        db.query(
            func.date(Alerte.date_envoi).label("jour"),
            Alerte.decision,
            func.count(Alerte.id),
        )
        .filter(Alerte.cooperative_id == cooperative.id, Alerte.date_envoi >= depuis_14j)
        .group_by("jour", Alerte.decision)
        .all()
    )
    par_jour = {}
    for jour, decision, total in lignes_14j:
        cle = jour.isoformat() if hasattr(jour, "isoformat") else str(jour)
        entree = par_jour.setdefault(cle, {"partez": 0, "attendez": 0, "evitez": 0})
        if decision == "PARTEZ":
            entree["partez"] += total
        elif decision == "ATTENDEZ":
            entree["attendez"] += total
        elif decision == "EVITEZ":
            entree["evitez"] += total
    alertes_par_jour_14j = [
        AlertesParJour(jour=jour, **valeurs) for jour, valeurs in sorted(par_jour.items())
    ]

    dernieres = (
        db.query(Alerte, Pecheur.nom)
        .join(Pecheur, Pecheur.id == Alerte.pecheur_id)
        .filter(Alerte.cooperative_id == cooperative.id)
        .order_by(Alerte.date_envoi.desc())
        .limit(20)
        .all()
    )
    dernieres_alertes = [
        AlerteJournalOut(
            id=alerte.id,
            pecheur_id=alerte.pecheur_id,
            pecheur_nom=nom,
            zone=alerte.zone,
            decision=alerte.decision,
            score=alerte.score,
            statut_sms=alerte.statut_sms,
            date_envoi=alerte.date_envoi,
        )
        for alerte, nom in dernieres
    ]

    return TableauBordCooperativeOut(
        cooperative=cooperative.nom,
        pecheurs_actifs=pecheurs_actifs or 0,
        alertes_30j=alertes_30j,
        sms_reellement_envoyes_30j=sms_envoyes_30j,
        taux_evitez_pct=taux_evitez_pct,
        repartition_decisions=repartition_decisions,
        alertes_par_jour_14j=alertes_par_jour_14j,
        dernieres_alertes=dernieres_alertes,
    )
