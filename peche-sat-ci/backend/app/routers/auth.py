from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.auth import creer_token, verifier_mot_de_passe
from app.database import get_db
from app.models import Cooperative
from app.schemas import ConnexionIn, TokenOut

router = APIRouter(prefix="/api/auth", tags=["auth"])


@router.post("/connexion", response_model=TokenOut)
def connexion(payload: ConnexionIn, db: Session = Depends(get_db)):
    cooperative = db.query(Cooperative).filter(Cooperative.email == payload.email).first()
    if not cooperative or not verifier_mot_de_passe(payload.mot_de_passe, cooperative.mot_de_passe_hash):
        raise HTTPException(status_code=401, detail="Email ou mot de passe incorrect.")
    return TokenOut(jeton=creer_token(cooperative.id), cooperative=cooperative.nom)
