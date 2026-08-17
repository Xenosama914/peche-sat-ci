import { useState } from "react";
import { Loader2, UserPlus } from "lucide-react";

import { inscrirePecheur } from "../api/client";

const CHAMPS_VIDES = { nom: "", telephone: "", type_pirogue: "", zone_rattachement: "" };

// Les zones connues du moteur. Un pêcheur rattaché à une zone hors de cette liste
// recevrait la lecture d'une autre mer, donc on propose au lieu de laisser deviner.
const ZONES = [
  "Abidjan",
  "Assinie",
  "Jacqueville",
  "Grand-Lahou",
  "Fresco",
  "Sassandra",
  "San Pédro",
  "Tabou",
];

export default function FormulaireInscription({ onInscrit }) {
  const [champs, setChamps] = useState(CHAMPS_VIDES);
  const [envoi, setEnvoi] = useState(false);
  const [erreur, setErreur] = useState(null);

  function majChamp(cle, valeur) {
    setChamps((c) => ({ ...c, [cle]: valeur }));
  }

  async function handleSubmit(e) {
    e.preventDefault();
    setEnvoi(true);
    setErreur(null);
    try {
      const pecheur = await inscrirePecheur(champs);
      setChamps(CHAMPS_VIDES);
      onInscrit?.(pecheur);
    } catch (err) {
      setErreur(err.response?.data?.detail || "L'inscription a échoué. Réessayez.");
    } finally {
      setEnvoi(false);
    }
  }

  return (
    <form onSubmit={handleSubmit} className="panneau p-5">
      <p className="kicker">INSCRIRE UN PÊCHEUR</p>
      <h2 className="mt-2 mb-4 text-[1.25rem]">Il recevra son mot chaque matin.</h2>

      <div className="grid grid-cols-1 gap-4 sm:grid-cols-2">
        <div>
          <label className="etiquette" htmlFor="p-nom">NOM COMPLET</label>
          <input
            id="p-nom"
            required
            className="saisie"
            value={champs.nom}
            onChange={(e) => majChamp("nom", e.target.value)}
            placeholder="Kouassi Yao"
          />
        </div>
        <div>
          <label className="etiquette" htmlFor="p-tel">TÉLÉPHONE</label>
          <input
            id="p-tel"
            required
            className="saisie"
            value={champs.telephone}
            onChange={(e) => majChamp("telephone", e.target.value)}
            placeholder="+225 07 00 00 00 00"
          />
        </div>
        <div>
          <label className="etiquette" htmlFor="p-pirogue">TYPE DE PIROGUE</label>
          <input
            id="p-pirogue"
            className="saisie"
            value={champs.type_pirogue}
            onChange={(e) => majChamp("type_pirogue", e.target.value)}
            placeholder="Pirogue motorisée"
          />
        </div>
        <div>
          <label className="etiquette" htmlFor="p-zone">ZONE DE SORTIE</label>
          <input
            id="p-zone"
            className="saisie"
            list="zones-connues"
            value={champs.zone_rattachement}
            onChange={(e) => majChamp("zone_rattachement", e.target.value)}
            placeholder="Jacqueville"
          />
          <datalist id="zones-connues">
            {ZONES.map((z) => (
              <option key={z} value={z} />
            ))}
          </datalist>
        </div>
      </div>

      {erreur && <p className="alerte alerte-erreur mt-4">{erreur}</p>}

      <button type="submit" disabled={envoi} className="bouton bouton-go mt-5">
        {envoi ? <Loader2 size={15} className="animate-spin" /> : <UserPlus size={15} />}
        Inscrire
      </button>
    </form>
  );
}
