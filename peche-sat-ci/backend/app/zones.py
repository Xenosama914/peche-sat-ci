"""Zones de sortie de la flotte artisanale ivoirienne.

Les pecheurs sont rattaches a une zone par un simple nom (Pecheur.zone_rattachement).
L'envoi matinal a besoin de coordonnees pour interroger le satellite, d'ou cette table.

Chaque point est place a une dizaine de kilometres AU LARGE du site de debarquement,
jamais sur la cote : les produits MODIS (chlorophylle) et OISST (temperature) masquent
les pixels terrestres, et un point pris sur la plage renvoie systematiquement
"DONNEES INDISPONIBLES".
"""

import unicodedata

# nom canonique -> (latitude, longitude, libelle affiche)
ZONES = {
    "abidjan": (5.10, -3.98, "Abidjan Sud"),
    "assinie": (5.00, -3.47, "Assinie"),
    "jacqueville": (5.05, -4.42, "Jacqueville"),
    "grand-lahou": (5.00, -5.02, "Grand-Lahou"),
    "fresco": (4.95, -5.57, "Fresco"),
    "sassandra": (4.83, -6.09, "Sassandra"),
    "san-pedro": (4.62, -6.63, "San Pedro"),
    "tabou": (4.30, -7.36, "Tabou"),
}

ZONE_PAR_DEFAUT = "abidjan"

# Ecritures courantes rencontrees dans les inscriptions, ramenees au nom canonique.
ALIAS = {
    "abidjan sud": "abidjan",
    "vridi": "abidjan",
    "port-bouet": "abidjan",
    "portbouet": "abidjan",
    "abidjan-vridi": "abidjan",
    "grand lahou": "grand-lahou",
    "grandlahou": "grand-lahou",
    "san pedro": "san-pedro",
    "sanpedro": "san-pedro",
    "san-pedro": "san-pedro",
}


def normaliser(nom: str | None) -> str:
    """Minuscules, sans accents, espaces reduits : 'San Pédro ' -> 'san pedro'."""
    if not nom:
        return ""
    sans_accent = "".join(
        c for c in unicodedata.normalize("NFD", nom) if unicodedata.category(c) != "Mn"
    )
    return " ".join(sans_accent.lower().split())


def resoudre(nom: str | None) -> tuple[str, float, float, str, bool]:
    """Retourne (cle, latitude, longitude, libelle, reconnue).

    Les pecheurs sont inscrits avec une zone en texte libre : "Jacqueville", mais
    aussi "Port de peche Jacqueville" ou "Port de peche d'Abidjan". On reconnait
    donc aussi le nom d'une zone CONTENU dans une phrase, sinon un pecheur de
    Jacqueville recevrait la lecture de la mer d'Abidjan, ce qui est pire que pas
    de message du tout.

    `reconnue` vaut False quand rien ne correspond : on retombe sur Abidjan et
    l'appelant doit le signaler plutot que de laisser croire que la lecture
    concerne la bonne zone.
    """
    texte = normaliser(nom)
    if not texte:
        lat, lon, libelle = ZONES[ZONE_PAR_DEFAUT]
        return ZONE_PAR_DEFAUT, lat, lon, libelle, False

    # 1. correspondance exacte, alias compris
    cle = ALIAS.get(texte, texte.replace(" ", "-"))
    if cle in ZONES:
        lat, lon, libelle = ZONES[cle]
        return cle, lat, lon, libelle, True

    # 2. le nom d'une zone contenu dans la phrase. Les cles les plus longues
    #    d'abord, pour que "grand lahou" gagne contre un eventuel "lahou".
    candidats: list[tuple[str, str]] = []
    for zone_cle in ZONES:
        candidats.append((zone_cle.replace("-", " "), zone_cle))
    for alias, zone_cle in ALIAS.items():
        candidats.append((alias, zone_cle))
    for aiguille, zone_cle in sorted(candidats, key=lambda c: len(c[0]), reverse=True):
        if aiguille in texte:
            lat, lon, libelle = ZONES[zone_cle]
            return zone_cle, lat, lon, libelle, True

    lat, lon, libelle = ZONES[ZONE_PAR_DEFAUT]
    return ZONE_PAR_DEFAUT, lat, lon, libelle, False


def liste_zones() -> list[dict]:
    """Les zones exposees a l'interface, pour que personne ne saisisse un nom au hasard."""
    return [
        {"cle": cle, "libelle": libelle, "latitude": lat, "longitude": lon}
        for cle, (lat, lon, libelle) in ZONES.items()
    ]
