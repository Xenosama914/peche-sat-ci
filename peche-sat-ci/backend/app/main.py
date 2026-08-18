import logging
import traceback
from contextlib import asynccontextmanager

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from app.config import ORIGINES_AUTORISEES
from app.database import Base, engine
from app.gee_service import init_gee
from app.routers import auth, cooperative, cron, inscription, pecheurs, score, sms


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Cree la table pecheurs si elle n'existe pas deja (idempotent, ne touche pas
    # aux tables existantes). Toute vraie evolution de schema doit passer par
    # une migration explicite, pas par create_all.
    Base.metadata.create_all(bind=engine)
    init_gee()
    yield


app = FastAPI(title="Peche-Sat CI API", lifespan=lifespan)

journal = logging.getLogger("peche-sat")


# ORDRE IMPORTANT : le middleware ajoute en dernier est le plus externe. Ce
# rattrapage doit donc etre declare AVANT le CORS, pour que la reponse d'erreur
# qu'il fabrique traverse encore le CORS et reparte avec ses en-tetes.
#
# Sans lui, une exception non rattrapee remonte au-dessus du CORS : le navigateur
# recoit une reponse sans en-tete d'origine et annonce "blocked by CORS policy".
# On cherche alors une panne de CORS qui n'existe pas, pendant que la vraie
# erreur reste invisible. Ici l'erreur revient lisible, cote navigateur comme
# dans les journaux Render.
@app.middleware("http")
async def rattraper_les_erreurs(request: Request, call_next):
    try:
        return await call_next(request)
    except Exception:
        journal.error("Erreur non rattrapee sur %s %s\n%s", request.method, request.url.path, traceback.format_exc())
        return JSONResponse(
            status_code=500,
            content={"detail": "Erreur interne du serveur. Le detail est dans les journaux du moteur."},
        )


app.add_middleware(
    CORSMiddleware,
    allow_origins=ORIGINES_AUTORISEES,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(pecheurs.router)
app.include_router(score.router)
app.include_router(sms.router)
app.include_router(auth.router)
app.include_router(cooperative.router)
app.include_router(cron.router)
app.include_router(inscription.router)


@app.get("/api/sante")
def sante():
    return {"statut": "ok"}
