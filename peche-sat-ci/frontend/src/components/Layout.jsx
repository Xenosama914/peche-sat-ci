import { LayoutDashboard, Users, Building2, LineChart } from "lucide-react";

const ONGLETS = [
  { id: "tableau-de-bord", label: "Tableau de bord", icon: LayoutDashboard },
  { id: "pecheurs", label: "Pêcheurs", icon: Users },
  { id: "offre", label: "Offre", icon: Building2 },
  { id: "espace-cooperative", label: "Espace Coopérative", icon: LineChart },
];

// La même marque que la vitrine : l'horizon et le satellite au-dessus.
function Marque() {
  return (
    <svg viewBox="0 0 32 32" width="26" height="26" aria-hidden="true" className="shrink-0">
      <rect width="32" height="32" rx="7" fill="#0e1a2b" />
      <path d="M3.5 24.5a12.5 12.5 0 0 1 25 0" fill="none" stroke="#2bc99b" strokeWidth="2.4" />
      <circle cx="16" cy="9" r="3.1" fill="#2bc99b" />
    </svg>
  );
}

export default function Layout({ page, onNavigate, children }) {
  return (
    <div className="min-h-screen">
      <header className="sticky top-0 z-30 border-b border-[var(--line)] bg-[rgba(6,13,24,0.92)] backdrop-blur-md">
        <div className="mx-auto flex max-w-6xl flex-wrap items-center gap-x-6 gap-y-3 px-4 py-3">
          <div className="mono flex items-center gap-2 text-[0.8rem] tracking-[0.1em] whitespace-nowrap">
            <Marque />
            PÊCHE-SAT CI
          </div>
          <nav className="flex flex-wrap gap-1.5">
            {ONGLETS.map(({ id, label, icon: Icon }) => {
              const actif = page === id;
              return (
                <button
                  key={id}
                  onClick={() => onNavigate(id)}
                  aria-current={actif ? "page" : undefined}
                  className={`mono flex items-center gap-1.5 rounded-lg px-3 py-1.5 text-[0.74rem] tracking-[0.06em] transition-colors ${
                    actif
                      ? "border border-[rgba(43,201,155,0.42)] bg-[rgba(9,32,26,0.7)] text-[var(--accent)]"
                      : "border border-transparent text-[var(--text-secondary)] hover:border-[var(--panel-edge)] hover:text-[var(--text-primary)]"
                  }`}
                >
                  <Icon size={14} />
                  {label}
                </button>
              );
            })}
          </nav>
        </div>
      </header>
      <main className="mx-auto max-w-6xl px-4 py-7">{children}</main>
      <footer className="mx-auto max-w-6xl px-4 pb-8">
        <p className="discret border-t border-[var(--line)] pt-4">
          Données publiques MODIS-Aqua (NASA), NOAA OISST, NOAA GFS. Les seuils sont un
          indicateur calibré à dire d'expert, pas une promesse de prise.
        </p>
      </footer>
    </div>
  );
}
