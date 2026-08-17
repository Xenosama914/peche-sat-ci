import { useState } from "react";

import EnvoiSMS from "../components/EnvoiSMS";
import FormulaireInscription from "../components/FormulaireInscription";
import ListePecheurs from "../components/ListePecheurs";

export default function Pecheurs({ score }) {
  const [pecheurSelectionne, setPecheurSelectionne] = useState(null);
  const [rafraichir, setRafraichir] = useState(0);

  const point = score ? { lat: score.latitude, lng: score.longitude } : null;

  return (
    <div className="space-y-6">
      <div>
        <p className="kicker">LA FLOTTE</p>
        <h1 className="mt-2 text-[clamp(1.6rem,3vw,2.3rem)]">Qui reçoit le message, et où il sort.</h1>
      </div>
      <FormulaireInscription onInscrit={() => setRafraichir((n) => n + 1)} />
      <ListePecheurs
        rafraichir={rafraichir}
        pecheurSelectionneId={pecheurSelectionne?.id}
        onSelectionner={setPecheurSelectionne}
      />
      <EnvoiSMS pecheur={pecheurSelectionne} point={point} />
    </div>
  );
}
