from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class PecheurCreate(BaseModel):
    nom: str
    telephone: str
    type_pirogue: str | None = None
    zone_rattachement: str | None = None


class PecheurOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    nom: str
    telephone: str
    type_pirogue: str | None
    zone_rattachement: str | None
    statut: str
    date_inscription: datetime


class ScoreOut(BaseModel):
    zone: str
    latitude: float
    longitude: float
    score: int
    decision: str
    couleur: str
    chlorophylle_mg_m3: float | None
    sst_celsius: float | None
    vent_m_s: float | None
    donnees_du: str | None
    sst_du: str | None = None
    message: str


class AlerteSMSIn(BaseModel):
    pecheur_id: int
    zone: str
    latitude: float
    longitude: float


class AlerteSMSOut(BaseModel):
    statut: str
    destinataire: str
    message: str
    detail: str
    message_id: str | None = None
    cout: str | None = None


class ConnexionIn(BaseModel):
    email: str
    mot_de_passe: str


class DemandeInscriptionIn(BaseModel):
    """Ce que la vitrine envoie. Les longueurs sont bornées : ce point d'entrée est
    public, donc il ne doit jamais accepter n'importe quoi de n'importe qui."""

    cooperative: str = Field(min_length=2, max_length=120)
    nom_contact: str = Field(min_length=2, max_length=120)
    contact: str = Field(min_length=4, max_length=160)
    zone: str | None = Field(default=None, max_length=120)
    nombre_pecheurs: str | None = Field(default=None, max_length=20)


class DemandeInscriptionOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    cooperative: str
    nom_contact: str
    contact: str
    zone: str | None
    nombre_pecheurs: str | None
    statut: str
    source: str
    date_creation: datetime


class TokenOut(BaseModel):
    jeton: str
    cooperative: str


class AlerteJournalOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    pecheur_id: int
    pecheur_nom: str
    zone: str | None
    decision: str | None
    score: int | None
    statut_sms: str | None
    date_envoi: datetime


class RepartitionDecision(BaseModel):
    decision: str
    total: int


class AlertesParJour(BaseModel):
    jour: str
    partez: int
    attendez: int
    evitez: int


class TableauBordCooperativeOut(BaseModel):
    cooperative: str
    pecheurs_actifs: int
    alertes_30j: int
    sms_reellement_envoyes_30j: int
    taux_evitez_pct: float
    repartition_decisions: list[RepartitionDecision]
    alertes_par_jour_14j: list[AlertesParJour]
    dernieres_alertes: list[AlerteJournalOut]
