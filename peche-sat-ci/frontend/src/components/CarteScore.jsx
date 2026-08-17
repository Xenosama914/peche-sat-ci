import { useState } from "react";
import { CircleMarker, MapContainer, Popup, TileLayer, useMapEvents } from "react-leaflet";
import { Loader2 } from "lucide-react";

import { obtenirScore } from "../api/client";

// Centré plus au sud que la côte : le geste utile est de cliquer EN MER, donc la
// mer doit occuper la carte, pas la terre.
const CENTRE_ABIDJAN = [4.85, -4.6];

const COULEURS = {
  vert: "#2bc99b",
  orange: "#e9a83c",
  rouge: "#e4574c",
  gris: "#8fa0b8",
};

function GestionClic({ onClic }) {
  useMapEvents({
    click(e) {
      onClic(e.latlng);
    },
  });
  return null;
}

export default function CarteScore({ onScore }) {
  const [point, setPoint] = useState(null);
  const [score, setScore] = useState(null);
  const [chargement, setChargement] = useState(false);
  const [erreur, setErreur] = useState(null);

  async function handleClic(latlng) {
    setPoint(latlng);
    setChargement(true);
    setErreur(null);
    try {
      const resultat = await obtenirScore(latlng.lat, latlng.lng, "Point sélectionné");
      setScore(resultat);
      onScore?.(resultat);
    } catch (err) {
      setErreur(
        err.response?.data?.detail || "Impossible de contacter le service satellite."
      );
      setScore(null);
    } finally {
      setChargement(false);
    }
  }

  return (
    <div className="panneau overflow-hidden">
      <div className="h-[440px] w-full">
        <MapContainer center={CENTRE_ABIDJAN} zoom={8} className="h-full w-full">
          {/* fond de carte sombre : la carte appartient au même monde que le reste */}
          <TileLayer
            attribution='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a>, &copy; <a href="https://carto.com/attributions">CARTO</a>'
            url="https://{s}.basemaps.cartocdn.com/dark_all/{z}/{x}/{y}{r}.png"
          />
          <GestionClic onClic={handleClic} />
          {point && (
            <CircleMarker
              center={point}
              radius={11}
              pathOptions={{
                color: score ? COULEURS[score.couleur] : "#8fa0b8",
                fillColor: score ? COULEURS[score.couleur] : "#8fa0b8",
                fillOpacity: 0.28,
                weight: 2.5,
              }}
            >
              <Popup>
                {chargement && <span className="mono text-xs">Lecture du satellite…</span>}
                {score && (
                  <div className="text-sm">
                    <p className="mono mb-1 text-[0.72rem] tracking-[0.1em]">{score.decision}</p>
                    <p className="secondaire">{score.message}</p>
                  </div>
                )}
                {erreur && <p className="text-[var(--danger)]">{erreur}</p>}
              </Popup>
            </CircleMarker>
          )}
        </MapContainer>
      </div>
      <div className="panneau-tete border-t border-b-0">
        <span>CLIQUEZ UNE ZONE EN MER POUR LA SONDER</span>
        {chargement && <Loader2 size={15} className="animate-spin text-[var(--accent)]" />}
      </div>
    </div>
  );
}
