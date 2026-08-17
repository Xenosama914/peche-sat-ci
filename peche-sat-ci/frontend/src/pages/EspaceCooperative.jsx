import { useEffect, useState } from "react";
import {
  Bar,
  BarChart,
  CartesianGrid,
  Cell,
  Legend,
  ResponsiveContainer,
  Tooltip,
  XAxis,
  YAxis,
} from "recharts";
import { Loader2, Lock, LogOut } from "lucide-react";

import {
  connexionCooperative,
  obtenirJeton,
  obtenirTableauBordCooperative,
  stockerJeton,
  supprimerJeton,
} from "../api/client";

// Palette de statut, alignée sur les puces de décision de toute la marque.
// Jamais réutilisée pour une série catégorielle générique.
const COULEUR_GOOD = "#2bc99b";
const COULEUR_WARNING = "#e9a83c";
const COULEUR_CRITICAL = "#e4574c";
const COULEUR_MUTED = "#8fa0b8";
const GRILLE = "#152238";
const ENCRE_AXE = "#7d90ab";

const COULEUR_DECISION = {
  PARTEZ: COULEUR_GOOD,
  ATTENDEZ: COULEUR_WARNING,
  EVITEZ: COULEUR_CRITICAL,
};

const PUCE_DECISION = {
  PARTEZ: "puce puce-go",
  ATTENDEZ: "puce puce-attente",
  EVITEZ: "puce puce-stop",
};

function couleurDecision(decision) {
  return COULEUR_DECISION[decision] || COULEUR_MUTED;
}

function FormulaireConnexion({ onConnecte }) {
  const [email, setEmail] = useState("");
  const [motDePasse, setMotDePasse] = useState("");
  const [erreur, setErreur] = useState(null);
  const [envoi, setEnvoi] = useState(false);

  async function handleSubmit(e) {
    e.preventDefault();
    setEnvoi(true);
    setErreur(null);
    try {
      const { jeton } = await connexionCooperative(email, motDePasse);
      stockerJeton(jeton);
      onConnecte();
    } catch (err) {
      setErreur(err.response?.data?.detail || "Connexion impossible.");
    } finally {
      setEnvoi(false);
    }
  }

  return (
    <div className="panneau mx-auto mt-6 max-w-md p-6">
      <div className="mb-1 flex items-center gap-2">
        <Lock size={15} className="text-[var(--accent)]" />
        <p className="kicker">ESPACE COOPÉRATIVE</p>
      </div>
      <h1 className="mt-2 mb-5 text-[1.5rem]">Votre flotte, vos alertes.</h1>

      <form onSubmit={handleSubmit} className="space-y-4">
        <div>
          <label className="etiquette" htmlFor="c-email">EMAIL</label>
          <input
            id="c-email"
            required
            type="email"
            className="saisie"
            value={email}
            onChange={(e) => setEmail(e.target.value)}
            autoComplete="email"
          />
        </div>
        <div>
          <label className="etiquette" htmlFor="c-mdp">MOT DE PASSE</label>
          <input
            id="c-mdp"
            required
            type="password"
            className="saisie"
            value={motDePasse}
            onChange={(e) => setMotDePasse(e.target.value)}
            autoComplete="current-password"
          />
        </div>
        {erreur && <p className="alerte alerte-erreur">{erreur}</p>}
        <button type="submit" disabled={envoi} className="bouton bouton-go w-full">
          {envoi && <Loader2 size={15} className="animate-spin" />}
          Se connecter
        </button>
      </form>
    </div>
  );
}

function TuileStat({ label, valeur, sousTexte }) {
  return (
    <div className="tuile">
      <p className="mono text-[0.66rem] tracking-[0.12em] text-[var(--text-muted)]">{label}</p>
      <p className="tuile-valeur">{valeur}</p>
      {sousTexte && <p className="discret mt-2">{sousTexte}</p>}
    </div>
  );
}

function CadreInfoBulle({ children }) {
  return (
    <div
      className="rounded-lg border px-3 py-2 text-xs"
      style={{
        background: "var(--panel-2)",
        borderColor: "var(--panel-edge)",
        boxShadow: "0 12px 40px rgba(3,7,15,.7)",
      }}
    >
      {children}
    </div>
  );
}

function InfoBulleDecisions({ active, payload }) {
  if (!active || !payload?.length) return null;
  const { decision, total } = payload[0].payload;
  return (
    <CadreInfoBulle>
      <p className="mono tracking-[0.1em]" style={{ color: couleurDecision(decision) }}>
        {decision}
      </p>
      <p className="secondaire mt-1">{total} alerte(s)</p>
    </CadreInfoBulle>
  );
}

function InfoBulleJour({ active, payload, label }) {
  if (!active || !payload?.length) return null;
  return (
    <CadreInfoBulle>
      <p className="mono mb-1 tracking-[0.1em] text-[var(--text-primary)]">{label}</p>
      {payload.map((entree) => (
        <p key={entree.dataKey} style={{ color: entree.color }}>
          {entree.value} — {entree.name}
        </p>
      ))}
    </CadreInfoBulle>
  );
}

function TableauBord({ donnees, onDeconnexion }) {
  const nomsDecision = { partez: "Partez", attendez: "Attendez", evitez: "Évitez" };

  return (
    <div className="space-y-6">
      <div className="flex flex-wrap items-end justify-between gap-4">
        <div>
          <p className="kicker">ESPACE COOPÉRATIVE</p>
          <h1 className="mt-2 text-[clamp(1.6rem,3vw,2.3rem)]">{donnees.cooperative}</h1>
        </div>
        <button onClick={onDeconnexion} className="bouton-discret">
          <LogOut size={14} /> SE DÉCONNECTER
        </button>
      </div>

      <div className="grid grid-cols-2 gap-4 lg:grid-cols-4">
        <TuileStat label="PÊCHEURS ACTIFS" valeur={donnees.pecheurs_actifs} />
        <TuileStat label="ALERTES ENVOYÉES (30J)" valeur={donnees.alertes_30j} />
        <TuileStat
          label="SMS RÉELLEMENT DÉLIVRÉS (30J)"
          valeur={donnees.sms_reellement_envoyes_30j}
          sousTexte="LE RESTE EST EN SIMULATION, MODE BAC À SABLE"
        />
        <TuileStat
          label="TAUX ÉVITEZ"
          valeur={`${donnees.taux_evitez_pct}%`}
          sousTexte="SORTIES DANGEREUSES DÉSAMORCÉES"
        />
      </div>

      <div className="grid grid-cols-1 gap-5 lg:grid-cols-2">
        <div className="panneau p-5">
          <h3 className="mb-4 text-[1.05rem]">Répartition des décisions, 30 derniers jours</h3>
          {donnees.repartition_decisions.length === 0 ? (
            <p className="secondaire text-sm">Aucune alerte sur la période.</p>
          ) : (
            <ResponsiveContainer width="100%" height={230}>
              <BarChart data={donnees.repartition_decisions} barCategoryGap="30%">
                <CartesianGrid vertical={false} stroke={GRILLE} />
                <XAxis
                  dataKey="decision"
                  tick={{ fill: ENCRE_AXE, fontSize: 11, fontFamily: "IBM Plex Mono, monospace" }}
                  axisLine={{ stroke: GRILLE }}
                  tickLine={false}
                />
                <YAxis
                  allowDecimals={false}
                  tick={{ fill: ENCRE_AXE, fontSize: 11, fontFamily: "IBM Plex Mono, monospace" }}
                  axisLine={false}
                  tickLine={false}
                  width={28}
                />
                <Tooltip content={<InfoBulleDecisions />} cursor={{ fill: "rgba(43,201,155,.06)" }} />
                <Bar dataKey="total" radius={[4, 4, 0, 0]} maxBarSize={48}>
                  {donnees.repartition_decisions.map((entree) => (
                    <Cell key={entree.decision} fill={couleurDecision(entree.decision)} />
                  ))}
                </Bar>
              </BarChart>
            </ResponsiveContainer>
          )}
        </div>

        <div className="panneau p-5">
          <h3 className="mb-4 text-[1.05rem]">Alertes par jour, 14 derniers jours</h3>
          {donnees.alertes_par_jour_14j.length === 0 ? (
            <p className="secondaire text-sm">Aucune alerte sur la période.</p>
          ) : (
            <ResponsiveContainer width="100%" height={230}>
              <BarChart data={donnees.alertes_par_jour_14j} barCategoryGap="20%">
                <CartesianGrid vertical={false} stroke={GRILLE} />
                <XAxis
                  dataKey="jour"
                  tick={{ fill: ENCRE_AXE, fontSize: 10, fontFamily: "IBM Plex Mono, monospace" }}
                  axisLine={{ stroke: GRILLE }}
                  tickLine={false}
                  tickFormatter={(j) => j.slice(5)}
                />
                <YAxis
                  allowDecimals={false}
                  tick={{ fill: ENCRE_AXE, fontSize: 11, fontFamily: "IBM Plex Mono, monospace" }}
                  axisLine={false}
                  tickLine={false}
                  width={28}
                />
                <Tooltip content={<InfoBulleJour />} cursor={{ fill: "rgba(43,201,155,.06)" }} />
                <Legend
                  formatter={(valeur) => (
                    <span style={{ color: ENCRE_AXE, fontSize: 11, fontFamily: "IBM Plex Mono, monospace" }}>
                      {/* Recharts passe le `name` de la série ("Partez"), pas la dataKey :
                          on cherche donc en minuscules, et on retombe sur la valeur brute
                          plutôt que d'afficher une légende vide. */}
                      {nomsDecision[String(valeur).toLowerCase()] || valeur}
                    </span>
                  )}
                />
                <Bar dataKey="partez" name="Partez" stackId="j" fill={COULEUR_GOOD} />
                <Bar dataKey="attendez" name="Attendez" stackId="j" fill={COULEUR_WARNING} />
                <Bar dataKey="evitez" name="Évitez" stackId="j" fill={COULEUR_CRITICAL} radius={[4, 4, 0, 0]} />
              </BarChart>
            </ResponsiveContainer>
          )}
        </div>
      </div>

      <div className="panneau overflow-hidden">
        <div className="panneau-tete">
          <span>DERNIÈRES ALERTES</span>
        </div>
        {donnees.dernieres_alertes.length === 0 ? (
          <p className="secondaire p-5 text-sm">Aucune alerte envoyée pour le moment.</p>
        ) : (
          <div className="overflow-x-auto">
            <table className="tableau">
              <thead>
                <tr>
                  <th>PÊCHEUR</th>
                  <th>DÉCISION</th>
                  <th>SCORE</th>
                  <th>SMS</th>
                  <th>DATE</th>
                </tr>
              </thead>
              <tbody>
                {donnees.dernieres_alertes.map((a) => (
                  <tr key={a.id}>
                    <td className="principal">{a.pecheur_nom}</td>
                    <td>
                      <span className={PUCE_DECISION[a.decision] || "puce puce-neutre"}>
                        {a.decision}
                      </span>
                    </td>
                    <td className="mono tabular-nums">{a.score}</td>
                    <td className="mono text-[0.8rem]">{String(a.statut_sms).toUpperCase()}</td>
                    <td className="mono text-[0.8rem]">
                      {new Date(a.date_envoi).toLocaleString("fr-FR")}
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        )}
      </div>
    </div>
  );
}

export default function EspaceCooperative() {
  const [connecte, setConnecte] = useState(Boolean(obtenirJeton()));
  const [donnees, setDonnees] = useState(null);
  const [chargement, setChargement] = useState(false);
  const [erreur, setErreur] = useState(null);

  async function charger() {
    setChargement(true);
    setErreur(null);
    try {
      setDonnees(await obtenirTableauBordCooperative());
    } catch (err) {
      if (err.response?.status === 401) {
        supprimerJeton();
        setConnecte(false);
      } else {
        setErreur("Impossible de charger le tableau de bord.");
      }
    } finally {
      setChargement(false);
    }
  }

  useEffect(() => {
    if (connecte) charger();
  }, [connecte]);

  function handleDeconnexion() {
    supprimerJeton();
    setConnecte(false);
    setDonnees(null);
  }

  if (!connecte) {
    return <FormulaireConnexion onConnecte={() => setConnecte(true)} />;
  }

  if (chargement && !donnees) {
    return (
      <div className="panneau flex items-center gap-2 p-5">
        <Loader2 size={15} className="animate-spin text-[var(--accent)]" />
        <span className="mono text-[0.76rem] tracking-[0.08em] text-[var(--text-secondary)]">
          CHARGEMENT DU TABLEAU DE BORD
        </span>
      </div>
    );
  }

  if (erreur) {
    return <p className="alerte alerte-erreur">{erreur}</p>;
  }

  return donnees ? <TableauBord donnees={donnees} onDeconnexion={handleDeconnexion} /> : null;
}
