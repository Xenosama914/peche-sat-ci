import { AlertTriangle } from "lucide-react";

import CarteScore from "../components/CarteScore";

const PUCE = {
  vert: "puce puce-go",
  orange: "puce puce-attente",
  rouge: "puce puce-stop",
  gris: "puce puce-neutre",
};

const SEUIL_DONNEES_ANCIENNES_JOURS = 30;

function joursDepuis(dateIso) {
  if (!dateIso) return null;
  return Math.floor((Date.now() - new Date(dateIso).getTime()) / 86_400_000);
}

function Mesure({ libelle, valeur, unite }) {
  return (
    <div className="flex items-baseline justify-between gap-3 border-b border-[var(--line)] py-2 last:border-b-0">
      <span className="mono text-[0.68rem] tracking-[0.12em] text-[var(--text-muted)]">{libelle}</span>
      <span className="mono text-[0.9rem] tabular-nums text-[var(--text-primary)]">
        {valeur != null ? `${valeur} ${unite}` : "—"}
      </span>
    </div>
  );
}

export default function TableauDeBord({ score, onScore }) {
  const ageChlA = score ? joursDepuis(score.donnees_du) : null;
  const chlADepassee = ageChlA != null && ageChlA > SEUIL_DONNEES_ANCIENNES_JOURS;

  return (
    <div className="space-y-6">
      <div>
        <p className="kicker">LECTURE DE LA MER</p>
        <h1 className="mt-2 text-[clamp(1.6rem,3vw,2.3rem)]">Sondez une zone avant de faire partir quelqu'un.</h1>
      </div>

      <div className="grid grid-cols-1 gap-5 lg:grid-cols-3">
        <div className="lg:col-span-2">
          <CarteScore onScore={onScore} />
        </div>

        <div className="panneau p-5">
          <p className="kicker">RÉSULTAT</p>

          {!score && (
            <p className="secondaire mt-3 text-sm">
              Aucune zone sondée. Cliquez un point en mer sur la carte, et la lecture
              s'affiche ici.
            </p>
          )}

          {score && (
            <div className="mt-3 space-y-4">
              <span className={PUCE[score.couleur]}>{score.decision}</span>

              <div className="flex items-baseline gap-2">
                <span className="font-[var(--display)] text-[2.6rem] font-extrabold leading-none tabular-nums">
                  {score.score}
                </span>
                <span className="mono text-[0.7rem] tracking-[0.12em] text-[var(--text-muted)]">SUR 100</span>
              </div>

              <p className="secondaire text-sm">{score.message}</p>

              <div>
                <Mesure libelle="CHLOROPHYLLE" valeur={score.chlorophylle_mg_m3} unite="mg/m³" />
                <Mesure libelle="TEMPÉRATURE" valeur={score.sst_celsius} unite="°C" />
                <Mesure libelle="VENT" valeur={score.vent_m_s} unite="m/s" />
              </div>

              {chlADepassee && (
                <div className="alerte alerte-attente">
                  <AlertTriangle size={15} className="mt-0.5 shrink-0" />
                  <span>
                    Chlorophylle ancienne de {ageChlA} jours : le capteur n'a pas été
                    réactualisé depuis le {score.donnees_du}. Le vent et la température,
                    eux, sont à jour.
                  </span>
                </div>
              )}

              <div className="discret space-y-0.5">
                {score.donnees_du && <p>CHLOROPHYLLE : DONNÉE DU {score.donnees_du}</p>}
                {score.sst_du && <p>TEMPÉRATURE : DONNÉE DU {score.sst_du}</p>}
              </div>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}
