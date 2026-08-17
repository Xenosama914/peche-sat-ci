import datetime

import jwt
from fastapi import Depends, HTTPException
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from passlib.context import CryptContext
from sqlalchemy.orm import Session

from app.config import JWT_SECRET
from app.database import get_db
from app.models import Cooperative

ALGORITHME = "HS256"
DUREE_TOKEN_HEURES = 12

_contexte_pwd = CryptContext(schemes=["bcrypt"], deprecated="auto")
_bearer = HTTPBearer()


def hacher_mot_de_passe(mot_de_passe: str) -> str:
    return _contexte_pwd.hash(mot_de_passe)


def verifier_mot_de_passe(mot_de_passe: str, hash_stocke: str) -> bool:
    return _contexte_pwd.verify(mot_de_passe, hash_stocke)


def creer_token(cooperative_id: int) -> str:
    expiration = datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(hours=DUREE_TOKEN_HEURES)
    return jwt.encode({"cooperative_id": cooperative_id, "exp": expiration}, JWT_SECRET, algorithm=ALGORITHME)


def cooperative_actuelle(
    identifiants: HTTPAuthorizationCredentials = Depends(_bearer),
    db: Session = Depends(get_db),
) -> Cooperative:
    try:
        payload = jwt.decode(identifiants.credentials, JWT_SECRET, algorithms=[ALGORITHME])
    except jwt.PyJWTError:
        raise HTTPException(status_code=401, detail="Session invalide ou expiree, reconnectez-vous.")
    cooperative = db.get(Cooperative, payload.get("cooperative_id"))
    if not cooperative:
        raise HTTPException(status_code=401, detail="Cooperative introuvable.")
    return cooperative
