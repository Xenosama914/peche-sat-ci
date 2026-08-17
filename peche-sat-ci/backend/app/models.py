from sqlalchemy import Column, Float, ForeignKey, Integer, String, DateTime, func
from sqlalchemy.orm import relationship

from app.database import Base


class Cooperative(Base):
    __tablename__ = "cooperatives"

    id = Column(Integer, primary_key=True, index=True)
    nom = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False, index=True)
    mot_de_passe_hash = Column(String, nullable=False)
    plan = Column(String, default="essai")
    statut_abonnement = Column(String, default="essai")
    date_creation = Column(DateTime(timezone=True), server_default=func.now())

    pecheurs = relationship("Pecheur", back_populates="cooperative")


class Pecheur(Base):
    __tablename__ = "pecheurs"

    id = Column(Integer, primary_key=True, index=True)
    nom = Column(String, nullable=False)
    telephone = Column(String, nullable=False)
    type_pirogue = Column(String)
    zone_rattachement = Column(String)
    statut = Column(String, default="actif")
    date_inscription = Column(DateTime(timezone=True), server_default=func.now())
    # Nullable : les pecheurs inscrits avant l'ajout du multi-tenant restent
    # rattaches a aucune cooperative jusqu'a affectation manuelle (migration additive).
    cooperative_id = Column(Integer, ForeignKey("cooperatives.id"), nullable=True)

    cooperative = relationship("Cooperative", back_populates="pecheurs")


class DemandeInscription(Base):
    """Une coopérative qui se manifeste depuis la vitrine.

    Volontairement séparée de la table `cooperatives` : une demande n'est pas un
    compte. Personne n'entre dans le service sans qu'un humain ait regardé.
    """

    __tablename__ = "demandes_inscription"

    id = Column(Integer, primary_key=True, index=True)
    cooperative = Column(String, nullable=False)
    nom_contact = Column(String, nullable=False)
    contact = Column(String, nullable=False)
    zone = Column(String)
    nombre_pecheurs = Column(String)
    statut = Column(String, default="nouvelle")  # nouvelle | traitee | refusee
    source = Column(String, default="vitrine")
    date_creation = Column(DateTime(timezone=True), server_default=func.now())


class Alerte(Base):
    __tablename__ = "alertes"

    id = Column(Integer, primary_key=True, index=True)
    pecheur_id = Column(Integer, ForeignKey("pecheurs.id"), nullable=False)
    cooperative_id = Column(Integer, ForeignKey("cooperatives.id"), nullable=True)
    zone = Column(String)
    latitude = Column(Float)
    longitude = Column(Float)
    decision = Column(String)
    score = Column(Integer)
    chlorophylle_mg_m3 = Column(Float, nullable=True)
    sst_celsius = Column(Float, nullable=True)
    vent_m_s = Column(Float, nullable=True)
    statut_sms = Column(String)
    message = Column(String)
    date_envoi = Column(DateTime(timezone=True), server_default=func.now())
