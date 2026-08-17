import { useState } from "react";
import { CheckCircle2, Loader2, MessageSquareWarning, Send } from "lucide-react";

import { envoyerAlerteSms } from "../api/client";

export default function EnvoiSMS({ pecheur, point }) {
  const [envoi, setEnvoi] = useState(false);
  const [resultat, setResultat] = useState(null);
  const [erreur, setErreur] = useState(null);

  const pret = Boolean(pecheur && point);

  async function handleEnvoyer() {
    setEnvoi(true);
    setErreur(null);
    setResultat(null);
    try {
      const reponse = await envoyerAlerteSms({
        pecheur_id: pecheur.id,
        zone: "Point sélectionné",
        latitude: point.lat,
        longitude: point.lng,
      });
      setResultat(reponse);
    } catch (err) {
      setErreur(err.response?.data?.detail || "Échec de l'envoi de l'alerte SMS.");
    } finally {
      setEnvoi(false);
    }
  }

  return (
    <div className="panneau p-5">
      <p className="kicker">ENVOI MANUEL</p>
      <h2 className="mt-2 mb-3 text-[1.25rem]">Prévenir un pêcheur maintenant.</h2>

      <p className="secondaire mb-4 text-sm">
        {pret ? (
          <>
            Le message partira vers <span className="text-[var(--text-primary)]">{pecheur.nom}</span>{" "}
            au <span className="mono text-[0.85rem]">{pecheur.telephone}</span>, pour la zone
            sondée sur la carte.
          </>
        ) : (
          "Choisissez un pêcheur dans la liste, puis sondez un point sur la carte du tableau de bord. L'envoi matinal, lui, part tout seul chaque matin."
        )}
      </p>

      <button onClick={handleEnvoyer} disabled={!pret || envoi} className="bouton bouton-go">
        {envoi ? <Loader2 size={15} className="animate-spin" /> : <Send size={15} />}
        Envoyer l'alerte
      </button>

      {resultat && (
        <div
          className={`alerte mt-4 ${
            resultat.statut === "envoye" ? "alerte-ok" : "alerte-attente"
          }`}
        >
          {resultat.statut === "envoye" ? (
            <CheckCircle2 size={15} className="mt-0.5 shrink-0" />
          ) : (
            <MessageSquareWarning size={15} className="mt-0.5 shrink-0" />
          )}
          <div>
            <p className="mono text-[0.72rem] tracking-[0.1em]">
              {resultat.statut === "envoye" ? "SMS ENVOYÉ" : "SIMULATION, MODE BAC À SABLE"}
            </p>
            <p className="mt-2 text-sm">« {resultat.message} »</p>
            <p className="discret mt-2">{resultat.detail}</p>
            {resultat.statut === "envoye" && (
              <p className="discret mt-1">
                ID {resultat.message_id} — COÛT {resultat.cout}
              </p>
            )}
          </div>
        </div>
      )}
      {erreur && <p className="alerte alerte-erreur mt-4">{erreur}</p>}
    </div>
  );
}
