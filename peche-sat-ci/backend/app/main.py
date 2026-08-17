from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

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
