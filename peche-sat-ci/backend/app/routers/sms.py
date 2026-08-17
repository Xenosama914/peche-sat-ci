from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.gee_service import calculer_score
from app.models import Alerte, Pecheur
from app.schemas import AlerteSMSIn, AlerteSMSOut
from app.sms_service import construire_message, envoyer_alerte

router = APIRouter(prefix="/api/sms", tags=["sms"])


@router.post("/alerte", response_model=AlerteSMSOut)
def envoyer_alerte_pecheur(payload: AlerteSMSIn, db: Session = Depends(get_db)):
    pecheur = db.get(Pecheur, payload.pecheur_id)
    if not pecheur:
        raise HTTPException(status_code=404, detail="Pecheur introuvable")

    try:
        score = calculer_score(payload.latitude, payload.longitude, payload.zone)
    except Exception as exc:
        raise HTTPException(status_code=502, detail=f"Erreur Google Earth Engine : {exc}")

    texte = construire_message(score["decision"], score["zone"], score["message"])
    resultat = envoyer_alerte(pecheur.telephone, texte)

    # Journalisation : c'est ce qui permet au dashboard coopérative de prouver la
    # valeur delivree (alertes envoyees, taux EVITEZ) — sans ca, rien n'est
    # reconstituable une fois le SMS parti.
    db.add(
        Alerte(
            pecheur_id=pecheur.id,
            cooperative_id=pecheur.cooperative_id,
            zone=score["zone"],
            latitude=payload.latitude,
            longitude=payload.longitude,
            decision=score["decision"],
            score=score["score"],
            chlorophylle_mg_m3=score.get("chlorophylle_mg_m3"),
            sst_celsius=score.get("sst_celsius"),
            vent_m_s=score.get("vent_m_s"),
            statut_sms=resultat["statut"],
            message=texte,
        )
    )
    db.commit()

    return resultat
