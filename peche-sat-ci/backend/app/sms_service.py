import http.client
import json
import re
import ssl
import urllib.parse

from app.config import AT_USERNAME, AT_API_KEY, AT_SENDER_ID

SEGMENT_MAX = 160  # GSM-7, un segment
AT_HOST = "api.sandbox.africastalking.com" if AT_USERNAME == "sandbox" else "api.africastalking.com"


def construire_message(decision: str, zone: str, message_score: str) -> str:
    sms = f"PECHE-SAT CI - {zone}: {decision}. {message_score}"
    if len(sms) > SEGMENT_MAX:
        sms = sms[: SEGMENT_MAX - 1] + "…"
    return sms


def normaliser_telephone(telephone: str) -> str:
    """Africa's Talking exige un format E.164 strict (+2250586971163), sans espaces
    ni tirets. Les pecheurs saisissent souvent leur numero au format local ivoirien
    (0X XX XX XX XX) : on le convertit en +225XXXXXXXXXX."""
    nettoye = re.sub(r"[^\d+]", "", telephone)
    if nettoye.startswith("00"):
        nettoye = "+" + nettoye[2:]
    elif nettoye.startswith("+"):
        pass
    elif nettoye.startswith("0"):
        nettoye = "+225" + nettoye[1:]
    else:
        nettoye = "+225" + nettoye
    return nettoye


def _envoyer_via_http_client(telephone: str, texte: str) -> dict:
    """Appelle l'API Africa's Talking directement en http.client plutot que via le
    SDK officiel (base sur requests/urllib3). Sur ce poste, requests echoue
    systematiquement avec SSLError WRONG_VERSION_NUMBER face a ce host alors qu'une
    connexion TLS brute (ssl.create_default_context) reussit a tous les coups :
    ca isole le probleme a la pile de connexion urllib3, pas au reseau ni a l'API AT."""
    champs = {
        "username": AT_USERNAME,
        "to": telephone,
        "message": texte,
        "bulkSMSMode": 1,
    }
    # Le sandbox AT rejette tout sender ID personnalise (InvalidSenderId) : c'est une
    # fonctionnalite premium qui doit etre approuvee sur un compte production.
    if AT_USERNAME != "sandbox" and AT_SENDER_ID:
        champs["from"] = AT_SENDER_ID
    corps = urllib.parse.urlencode(champs)
    headers = {
        "Accept": "application/json",
        "Content-Type": "application/x-www-form-urlencoded",
        "apiKey": AT_API_KEY,
    }
    conn = http.client.HTTPSConnection(AT_HOST, 443, timeout=15, context=ssl.create_default_context())
    try:
        conn.request("POST", "/version1/messaging", body=corps, headers=headers)
        reponse = conn.getresponse()
        donnees = json.loads(reponse.read().decode())
    finally:
        conn.close()
    return donnees


def envoyer_alerte(telephone: str, texte: str) -> dict:
    """Envoie le SMS via Africa's Talking Sandbox.
    En sandbox, l'envoi echoue si le numero n'est pas enregistre dans le simulateur AT :
    on catch cette erreur et on renvoie un statut 'simulation' plutot qu'un 500."""
    telephone = normaliser_telephone(telephone)
    try:
        donnees = _envoyer_via_http_client(telephone, texte)
        recipients = donnees.get("SMSMessageData", {}).get("Recipients", [])
        if recipients and recipients[0].get("status") == "Success":
            return {
                "statut": "envoye",
                "destinataire": telephone,
                "message": texte,
                "detail": "SMS envoye via Africa's Talking Sandbox.",
                "message_id": recipients[0].get("messageId"),
                "cout": recipients[0].get("cost"),
            }
        detail = recipients[0].get("status") if recipients else donnees
        return {
            "statut": "simulation",
            "destinataire": telephone,
            "message": texte,
            "detail": f"Numero non verifie dans le simulateur AT ({detail}). Simulation enregistree cote serveur.",
        }
    except Exception as exc:
        return {
            "statut": "simulation",
            "destinataire": telephone,
            "message": texte,
            "detail": f"Erreur Africa's Talking Sandbox : {exc}. Simulation enregistree cote serveur.",
        }
