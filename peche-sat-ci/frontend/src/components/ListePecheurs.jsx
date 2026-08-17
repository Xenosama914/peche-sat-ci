import { useEffect, useState } from "react";
import { Loader2, RefreshCw } from "lucide-react";

import { listerPecheurs } from "../api/client";

export default function ListePecheurs({ onSelectionner, pecheurSelectionneId, rafraichir }) {
  const [pecheurs, setPecheurs] = useState([]);
  const [chargement, setChargement] = useState(true);
  const [erreur, setErreur] = useState(null);

  async function charger() {
    setChargement(true);
    setErreur(null);
    try {
      setPecheurs(await listerPecheurs());
    } catch {
      setErreur("Impossible de charger la liste des pêcheurs depuis le serveur.");
    } finally {
      setChargement(false);
    }
  }

  useEffect(() => {
    charger();
  }, [rafraichir]);

  if (chargement) {
    return (
      <div className="panneau flex items-center gap-2 p-5">
        <Loader2 size={15} className="animate-spin text-[var(--accent)]" />
        <span className="mono text-[0.76rem] tracking-[0.08em] text-[var(--text-secondary)]">
          CHARGEMENT DES PÊCHEURS
        </span>
      </div>
    );
  }

  if (erreur) {
    return <p className="alerte alerte-erreur">{erreur}</p>;
  }

  if (pecheurs.length === 0) {
    return (
      <div className="panneau p-5">
        <p className="secondaire text-sm">
          Aucun pêcheur inscrit. Le formulaire ci-dessus est le point de départ.
        </p>
      </div>
    );
  }

  return (
    <div className="panneau overflow-hidden">
      <div className="panneau-tete">
        <span>{pecheurs.length} PÊCHEUR(S) INSCRIT(S)</span>
        <button onClick={charger} className="bouton-discret" aria-label="Rafraîchir la liste">
          <RefreshCw size={14} />
          RAFRAÎCHIR
        </button>
      </div>
      <div className="overflow-x-auto">
        <table className="tableau">
          <thead>
            <tr>
              <th>NOM</th>
              <th>TÉLÉPHONE</th>
              <th>PIROGUE</th>
              <th>ZONE</th>
              <th>STATUT</th>
            </tr>
          </thead>
          <tbody>
            {pecheurs.map((p) => (
              <tr
                key={p.id}
                onClick={() => onSelectionner?.(p)}
                className={`cliquable ${pecheurSelectionneId === p.id ? "selectionnee" : ""}`}
              >
                <td className="principal">{p.nom}</td>
                <td className="mono text-[0.82rem]">{p.telephone}</td>
                <td>{p.type_pirogue || "—"}</td>
                <td>{p.zone_rattachement || "—"}</td>
                <td>
                  <span className={`puce ${p.statut === "actif" ? "puce-go" : "puce-neutre"}`}>
                    {String(p.statut).toUpperCase()}
                  </span>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}
