import datetime
import os
import tempfile

import ee

from app.config import GEE_SERVICE_ACCOUNT, GEE_KEY_FILE, GEE_KEY_JSON

_initialized = False


def _chemin_de_la_cle() -> str:
    """Le chemin du fichier de cle Earth Engine.

    En local c'est GEE_KEY_FILE. En ligne, l'hebergeur ne stocke que des variables :
    on recoit alors le contenu JSON dans GEE_KEY_JSON et on l'ecrit dans un fichier
    temporaire, lisible par le seul proprietaire du processus.
    """
    if GEE_KEY_JSON:
        fd, chemin = tempfile.mkstemp(suffix=".json", prefix="gee-key-")
        with os.fdopen(fd, "w", encoding="utf-8") as f:
            f.write(GEE_KEY_JSON)
        os.chmod(chemin, 0o600)
        return chemin
    if not GEE_KEY_FILE:
        raise RuntimeError(
            "Aucune cle Earth Engine : renseignez GEE_KEY_FILE (chemin, en local) "
            "ou GEE_KEY_JSON (contenu du fichier, en ligne)."
        )
    return GEE_KEY_FILE


def init_gee():
    """Initialise la connexion Google Earth Engine avec le compte de service.
    Idempotent : ne relance pas l'auth si deja fait (utile avec --reload)."""
    global _initialized
    if _initialized:
        return
    credentials = ee.ServiceAccountCredentials(GEE_SERVICE_ACCOUNT, _chemin_de_la_cle())
    ee.Initialize(credentials)
    _initialized = True


# Seuils calibres a dire d'expert (proxy), pas un modele de biomasse valide.
# Chl-a haute = eau productive = poissons probables. Vent fort = danger mer.
CHLA_SEUIL_BON = 0.5  # mg/m3
CHLA_SEUIL_MOYEN = 0.15
VENT_SEUIL_DANGER = 10.0  # m/s (~36 km/h)
VENT_SEUIL_VIGILANCE = 7.0


NB_IMAGES_OCEAN = 20  # composite sur les N dernieres images dispo (pas une fenetre calendaire fixe :
# le catalogue GEE de NASA/OCEANDATA/MODIS-Aqua/L3SMI a des trous d'ingestion de plusieurs mois,
# une fenetre "aujourd'hui - 12 jours" peut donc tomber sur une periode totalement vide).
NB_JOURS_VENT = 5


def calculer_score(latitude: float, longitude: float, zone: str) -> dict:
    """Calcule un indice de conditions de peche (Habitat Suitability Index proxy)
    a partir de Chl-a (MODIS-Aqua), SST (NOAA OISST) et du vent de surface (NOAA GFS).
    Retourne un score 0-100 et une decision GO / ATTENDEZ / EVITEZ."""
    init_gee()

    point = ee.Geometry.Point([longitude, latitude])

    # Chl-a : NASA/OCEANDATA (Aqua et Terra) n'est plus ingere dans le catalogue GEE
    # depuis fin nov. 2025 (verifie empiriquement, pas de source de remplacement
    # fiable pour un proxy productivite calibre dans le budget du hackathon) : on
    # prend le meilleur composite disponible et on expose sa date pour rester honnete.
    chla_coll = (
        ee.ImageCollection("NASA/OCEANDATA/MODIS-Aqua/L3SMI")
        .sort("system:time_start", False)
        .limit(NB_IMAGES_OCEAN)
    )
    derniere_image_chla = chla_coll.first()
    chla = chla_coll.select("chlor_a").mean()

    # SST : NOAA OISST (CDR) est mis a jour en quasi temps reel (quelques jours de
    # retard), contrairement au produit MODIS ci-dessus. Bande "sst" encodee en
    # int16 avec un facteur d'echelle de 0.01 (convention NOAA).
    sst_coll = ee.ImageCollection("NOAA/CDR/OISST/V2_1").sort("system:time_start", False).limit(1)
    derniere_image_sst = sst_coll.first()
    sst_img = sst_coll.select("sst").mean().multiply(0.01)

    # ERA5-Land ne couvre que les terres (pixels ocean masques a null) : inutilisable
    # pour du vent en mer. GFS0P25 (NOAA) couvre le globe entier et est mis a jour
    # toutes les 6h ; forecast_hours == 0 = analyse "temps reel", pas une prevision.
    aujourdhui = datetime.date.today()
    debut_vent = (aujourdhui - datetime.timedelta(days=NB_JOURS_VENT)).isoformat()
    fin_vent = (aujourdhui + datetime.timedelta(days=1)).isoformat()
    vent = (
        ee.ImageCollection("NOAA/GFS0P25")
        .filterDate(debut_vent, fin_vent)
        .filter(ee.Filter.eq("forecast_hours", 0))
        .sort("system:time_start", False)
        .limit(1)
        .select(["u_component_of_wind_10m_above_ground", "v_component_of_wind_10m_above_ground"])
        .mean()
        .rename(["u_component_of_wind_10m", "v_component_of_wind_10m"])
    )

    stats_chla = chla.reduceRegion(
        reducer=ee.Reducer.mean(), geometry=point, scale=4000, bestEffort=True
    ).getInfo()
    stats_sst = sst_img.reduceRegion(
        reducer=ee.Reducer.mean(), geometry=point, scale=27000, bestEffort=True
    ).getInfo()
    stats_vent = vent.reduceRegion(
        reducer=ee.Reducer.mean(), geometry=point, scale=9000, bestEffort=True
    ).getInfo()
    date_chla = derniere_image_chla.get("system:time_start").getInfo()
    date_sst = derniere_image_sst.get("system:time_start").getInfo()

    chlor_a = stats_chla.get("chlor_a")
    sst = stats_sst.get("sst")
    u = stats_vent.get("u_component_of_wind_10m")
    v = stats_vent.get("v_component_of_wind_10m")
    vent_vitesse = (u ** 2 + v ** 2) ** 0.5 if u is not None and v is not None else None

    def _vers_date(ms):
        return datetime.datetime.fromtimestamp(ms / 1000, datetime.timezone.utc).date().isoformat() if ms else None

    return _decider(
        zone, latitude, longitude, chlor_a, sst, vent_vitesse, donnees_du=_vers_date(date_chla)
    ) | {"sst_du": _vers_date(date_sst)}


def _decider(zone, latitude, longitude, chlor_a, sst, vent_vitesse, donnees_du=None) -> dict:
    # Pas de donnee exploitable (nuages, zone hors couverture satellite) -> on ne ment pas au pecheur.
    if chlor_a is None or sst is None:
        return {
            "zone": zone,
            "latitude": latitude,
            "longitude": longitude,
            "score": 0,
            "decision": "DONNEES INDISPONIBLES",
            "couleur": "gris",
            "chlorophylle_mg_m3": chlor_a,
            "sst_celsius": sst,
            "vent_m_s": vent_vitesse,
            "donnees_du": donnees_du,
            "message": "Pas de donnee satellite exploitable sur cette zone aujourd'hui (couverture nuageuse probable). Reessayez demain.",
        }

    # Score productivite (0-70) base sur Chl-a
    if chlor_a >= CHLA_SEUIL_BON:
        score_prod = 70
    elif chlor_a >= CHLA_SEUIL_MOYEN:
        score_prod = 40
    else:
        score_prod = 15

    # Score securite (0-30) base sur le vent
    if vent_vitesse is None:
        score_secu = 15
    elif vent_vitesse < VENT_SEUIL_VIGILANCE:
        score_secu = 30
    elif vent_vitesse < VENT_SEUIL_DANGER:
        score_secu = 15
    else:
        score_secu = 0

    score = score_prod + score_secu

    # Le danger mer est prioritaire : vent fort => EVITEZ, quelle que soit la productivite.
    if vent_vitesse is not None and vent_vitesse >= VENT_SEUIL_DANGER:
        decision, couleur = "EVITEZ", "rouge"
        message = f"Vent fort ({vent_vitesse:.1f} m/s) : mer dangereuse pour une pirogue. Ne sortez pas aujourd'hui."
    elif score >= 66:
        decision, couleur = "PARTEZ", "vert"
        message = f"Bonnes conditions en {zone} : eau productive (chl-a {chlor_a:.2f} mg/m3) et mer calme."
    elif score >= 35:
        decision, couleur = "ATTENDEZ", "orange"
        message = f"Conditions moyennes en {zone}. Prudence, verifiez la meteo avant de partir loin."
    else:
        decision, couleur = "EVITEZ", "rouge"
        message = f"Faible productivite en {zone} (chl-a {chlor_a:.2f} mg/m3). Sortie peu rentable aujourd'hui."

    return {
        "zone": zone,
        "latitude": latitude,
        "longitude": longitude,
        "score": score,
        "decision": decision,
        "couleur": couleur,
        "chlorophylle_mg_m3": round(chlor_a, 3) if chlor_a is not None else None,
        "sst_celsius": round(sst, 2) if sst is not None else None,
        "vent_m_s": round(vent_vitesse, 2) if vent_vitesse is not None else None,
        "donnees_du": donnees_du,
        "message": message,
    }
