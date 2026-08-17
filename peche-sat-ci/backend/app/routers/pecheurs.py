from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import Pecheur
from app.schemas import PecheurCreate, PecheurOut

router = APIRouter(prefix="/api/pecheurs", tags=["pecheurs"])


@router.get("", response_model=list[PecheurOut])
def lister_pecheurs(db: Session = Depends(get_db)):
    return db.query(Pecheur).order_by(Pecheur.date_inscription.desc()).all()


@router.post("", response_model=PecheurOut, status_code=201)
def inscrire_pecheur(payload: PecheurCreate, db: Session = Depends(get_db)):
    pecheur = Pecheur(**payload.model_dump(), statut="actif")
    db.add(pecheur)
    db.commit()
    db.refresh(pecheur)
    return pecheur


@router.get("/{pecheur_id}", response_model=PecheurOut)
def obtenir_pecheur(pecheur_id: int, db: Session = Depends(get_db)):
    pecheur = db.get(Pecheur, pecheur_id)
    if not pecheur:
        raise HTTPException(status_code=404, detail="Pecheur introuvable")
    return pecheur
