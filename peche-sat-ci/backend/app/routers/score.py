from fastapi import APIRouter, HTTPException

from app.gee_service import calculer_score
from app.schemas import ScoreOut

router = APIRouter(prefix="/api/score", tags=["score"])


@router.get("", response_model=ScoreOut)
def obtenir_score(latitude: float, longitude: float, zone: str = "Zone selectionnee"):
    try:
        return calculer_score(latitude, longitude, zone)
    except Exception as exc:
        raise HTTPException(
            status_code=502,
            detail=f"Erreur Google Earth Engine : {exc}",
        )
