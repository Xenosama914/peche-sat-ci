import { Check, ShieldCheck } from "lucide-react";

const PILIERS = [
  {
    titre: "Pêcher plus intelligemment",
    detail: "Chlorophylle-a, température de surface, thermocline.",
  },
  { titre: "Pêcher plus vite", detail: "Itinéraires optimisés, courants de surface." },
  {
    titre: "Pêcher plus efficacement",
    detail: "Cartes d'habitats favorables (proxy biomasse).",
  },
  {
    titre: "Pêcher plus sûrement",
    detail: "Alertes vent fort et mer dangereuse en temps réel.",
  },
];

const INCLUS = [
  "Alertes SMS illimitées pour tous les membres",
  "Tableau de bord cartographique en temps réel",
  "Registre des pêcheurs et suivi des sorties",
];

export default function Cooperative() {
  return (
    <div className="space-y-6">
      <div>
        <p className="kicker">L'OFFRE</p>
        <h1 className="mt-2 max-w-[20ch] text-[clamp(1.6rem,3vw,2.3rem)]">
          Le pêcheur ne paie jamais. La coopérative s'abonne.
        </h1>
        <p className="secondaire mt-4 max-w-[62ch] text-sm">
          Pendant le pilote, l'accès est gratuit pour les coopératives retenues. L'État et
          les ONG financent cette phase pour la flotte artisanale. La facturation viendra
          ensuite, et elle sera annoncée avant, jamais après.
        </p>
      </div>

      <div className="grid grid-cols-1 gap-4 sm:grid-cols-2">
        {PILIERS.map((p) => (
          <div key={p.titre} className="panneau p-5">
            <h3 className="text-[1.05rem]">{p.titre}</h3>
            <p className="secondaire mt-2 text-sm">{p.detail}</p>
          </div>
        ))}
      </div>

      <div className="panneau relative overflow-hidden p-6">
        <div
          aria-hidden="true"
          className="absolute inset-x-0 top-0 h-[2px] opacity-60"
          style={{
            background:
              "linear-gradient(90deg,#12203a 0%,#17506e 26%,#1a8f8a 52%,#2bc99b 74%,#e9a83c 100%)",
          }}
        />
        <div className="mb-3 flex items-center gap-2">
          <ShieldCheck size={17} className="text-[var(--accent)]" />
          <h3 className="text-[1.15rem]">Abonnement coopérative</h3>
        </div>
        <ul className="space-y-2.5">
          {INCLUS.map((item) => (
            <li key={item} className="secondaire flex items-baseline gap-2.5 text-sm">
              <Check size={15} className="shrink-0 translate-y-[2px] text-[var(--accent)]" />
              {item}
            </li>
          ))}
        </ul>
        <p className="discret mt-5">TARIF ANNONCÉ À LA FIN DU PILOTE.</p>
      </div>
    </div>
  );
}
