import os
from dotenv import load_dotenv

load_dotenv()

GEE_SERVICE_ACCOUNT = os.getenv("GEE_SERVICE_ACCOUNT")
GEE_KEY_FILE = os.getenv("GEE_KEY_FILE")
# En local, la cle Earth Engine est un FICHIER (GEE_KEY_FILE). Un hebergeur, lui,
# ne sait stocker qu'une variable : on accepte donc aussi le CONTENU du fichier
# dans GEE_KEY_JSON, que gee_service ecrit sur disque au demarrage.
GEE_KEY_JSON = os.getenv("GEE_KEY_JSON")
AT_USERNAME = os.getenv("AT_USERNAME")
AT_API_KEY = os.getenv("AT_API_KEY")
AT_SENDER_ID = os.getenv("AT_SENDER_ID")
DATABASE_URL = os.getenv("DATABASE_URL")
JWT_SECRET = os.getenv("JWT_SECRET")

# Secret partage avec le declencheur externe de l'envoi matinal. Volontairement
# NON obligatoire : sans lui l'application demarre normalement et seul l'endpoint
# cron refuse de servir, plutot que d'empecher tout le backend de booter.
CRON_SECRET = os.getenv("CRON_SECRET")

# Origines autorisees a appeler l'API depuis un navigateur (la vitrine, le tableau
# de bord). Liste separee par des virgules dans l'environnement de production.
ORIGINES_AUTORISEES = [
    o.strip()
    for o in os.getenv(
        "ORIGINES_AUTORISEES",
        "http://localhost:5173,http://127.0.0.1:5173,http://localhost:8899,http://127.0.0.1:8899",
    ).split(",")
    if o.strip()
]

if not DATABASE_URL:
    raise RuntimeError("DATABASE_URL manquant dans backend/.env")
if not JWT_SECRET:
    raise RuntimeError("JWT_SECRET manquant dans backend/.env")

# Neon exige SSL. On force sslmode=require si l'URL ne le precise pas deja.
if "sslmode" not in DATABASE_URL:
    separator = "&" if "?" in DATABASE_URL else "?"
    DATABASE_URL = f"{DATABASE_URL}{separator}sslmode=require"
