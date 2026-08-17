# Design Package: Pêche-Sat CI

Tier 1, single journey. One 6 second generated shot scrubbed by scroll.
Written before generation. Consumed by the build. Every line of copy ships verbatim.
Site language: French. Audience: Ivorian fishing cooperatives, plus the state and NGO
partners who fund the pilot.

---

## 1. The brand premise

One word before you go out. That is the whole product and the whole site.
Pêche-Sat CI turns three public satellite measurements into a single word a fisherman
reads on a basic phone before pushing the pirogue into the water: PARTEZ, ATTENDEZ,
ÉVITEZ. The site teaches that one word and sells the subscription that carries it.
Every section serves it: the cost of an empty trip, how the word is made, what happens
on the day the word cannot be made honestly, and who pays for it. Nothing else belongs
on the page.

The register: plain, direct, serious, never dramatic. This is a service that talks about
people not coming home. It never sells that. It states it.

---

## 2. The palette as CSS tokens

Sampled from the descent: cold indigo at orbit, the cyan of the atmospheric limb, the
jade of productive water, warm dawn light on the swell. Values finalized against the
approved footage after the video gate.

```css
:root{
  --canvas:#060d18;         /* deep indigo sea-black, tinted blue, never pure black */
  --canvas-deep:#03070f;    /* the fixed background environment layer */
  --panel:#0e1a2b;          /* cards and raised surfaces */
  --panel-edge:#1c2c44;     /* panel borders, interactive borders get --line-strong */
  --line:#152238;           /* hairline dividers, decoration only */
  --line-strong:#3a5175;    /* interactive borders, 3:1 against canvas minimum */
  --accent:#2bc99b;         /* sea jade: the CTA, focus states, the PARTEZ chip */
  --accent-hover:#4fd9b0;
  --accent-muted:#153f36;   /* borders, glows, particles at whisper level */
  --warn:#e9a83c;           /* ATTENDEZ only */
  --danger:#e4574c;         /* ÉVITEZ only */
  --text-primary:#eaf0f7;   /* warm off-white, never pure white */
  --text-secondary:#93a6c0;
}
```

**Deviation said out loud:** dark canvas with a green accent sits near a look the standard
bans (near-black with acid green). This is not that look and it is earned three ways. The
canvas is a blue indigo pulled from the ocean at depth, not a neutral near-black. The green
is a desaturated sea jade sampled from productive water, not an acid lime. And the green is
the product's own semantics: PARTEZ is green in the running app, so the call to action being
that same green is the page arguing its own point. The accent stays rare: the CTA, focus
rings, the PARTEZ chip, and one emphasis per section.

---

## 3. The type trio

- **Display: Bricolage Grotesque**, weights 700 and 800. Technical and editorial with real
  character, full French accent coverage.
- **Body: Public Sans**, weights 400 and 600. Quiet, legible at small sizes, clean accents.
- **Mono: IBM Plex Mono**, weights 400 and 500. The instrument voice: HUD readouts, kickers,
  units, coordinates, decision chips.

Not Inter, not Roboto. Fonts trimmed to these five weights, with preconnect.

---

## 4. The band map

Hero height 700vh, so the scroll range is 600vh. Ranges are starting points, validated by
the flick test.

**Final ranges after the footage arrived.** The delivered film reaches the sea at about 0.47
and blows out to near white fog between 0.33 and 0.45, so the ranges below were re-cut
against it and validated by the flick test and the worst frame audit:
band 1 `0.00 to 0.16`, band 2 `0.21 to 0.40`, band 3 `0.46 to 0.68`, band 4 `0.74 to 1.00`.
Bands 3 and 4 moved to the BOTTOM of the frame, because in this footage the upper third is
bright dawn sky and the lower two thirds is dark jade water. Per band scrim peaks, each
tuned against its own worst frame: band 1 `0.92` (wide, the headline's ends sat on the bright
column), band 2 `0.88` (the white fog), band 3 `0.74`, band 4 `0.76`. Measured worst pixel
contrast after tuning: 3.54, 4.20, 6.57, 7.13 against a 3.5 floor.

| Band | Range (as designed) | Footage moment | Copy (verbatim) | Entrance |
|---|---|---|---|---|
| 1 | 0.00 to 0.19 | High orbit. The curved limb of the Earth, the Gulf of Guinea under cloud, the atmosphere glowing at the edge. | kicker: `GOLFE DE GUINÉE  05°10'N  004°02'W`<br>headline: "Chaque matin, la même question."<br>subline: "Est-ce que je sors aujourd'hui ?" | Blur to sharp. Focus arrives the way the atmosphere clears. Band 1 gets the one time load ramp so it opens settled. |
| 2 | 0.23 to 0.44 | Falling through the cloud layer. Wisps streak past the lens, a beat of blur, light scattering. | headline: "La réponse est déjà au-dessus de vous."<br>subline: "À 705 kilomètres, un satellite lit la couleur de votre mer." | Drift down. Words start above their resting place and fall into it, echoing the descent. |
| 3 | 0.48 to 0.68 | Below the cloud. The ocean's colour resolves, the swell reads as water, dawn light arrives from the east. | headline: "La couleur de l'eau dit où est le poisson."<br>subline: "Le vent dit si vous rentrerez." | Scatter. Characters assemble from seeded offsets, echoing plankton gathering into a bloom. |
| 4 | 0.74 to 1.00 | The settle. Resting just above the swell at dawn, a distant pirogue on the water, horizon glowing. | headline: "Un mot avant de partir."<br>subline: "PARTEZ, ATTENDEZ ou ÉVITEZ. Par SMS, sur le téléphone que vous avez déjà."<br>CTA: "Inscrire ma coopérative"<br>secondary: "Voir comment ça marche" | Word by word rise into a staged settle: headline words rise in reading order, then the subline, then the CTA row. Three arrivals, one band. |

The action lane is the centre of the frame the whole way down (the Earth, then the cloud
column, then the water). Captions live in the upper third for bands 1 to 3 and centre low
for the settle, kept clear of the descent's centre column.

**The signature element: the descent HUD.** A fixed mono readout in the hero's lower left,
scrubbed by the same progress value: altitude counting 705 km down to 0 m across the fall,
with the layer label changing as it passes (ORBITE, ATMOSPHÈRE, NUAGES, SURFACE). Once the
film reaches the sea at 0.47 the altitude has nothing left to say, so the instrument starts
reporting the reading instead: `CHL-A 0,62`, then `VENT 5,1 m/s`, then `SCORE 78/100`. At
the settle it resolves into the PARTEZ chip. This is where the boldness budget is spent. Remove it and the
hero loses its argument, which is the test of a real signature. It hides under
`(max-height: 560px)`.

---

## 5. The static hero copy block

For phones, portrait tablets, and reduced motion. Composed over the ending frame.

- kicker: `PÊCHE-SAT CI`
- headline: "Un mot avant de partir."
- subline: "Le satellite lit la mer chaque matin. Votre téléphone reçoit la réponse : PARTEZ, ATTENDEZ ou ÉVITEZ."
- CTA: "Inscrire ma coopérative"
- secondary: "Voir comment ça marche"

---

## 6. The below-fold outline

Every section funnels to one anchor: `#inscription`, the cooperative sign-up form.

### S1. Le prix d'une sortie

- kicker: `CE QUE COÛTE UNE SORTIE`
- headline: "Sortir coûte cher avant même d'avoir pris un poisson."
- body: "Le carburant d'une sortie à la journée pèse entre 37 000 et 90 000 F CFA, soit plus des deux tiers du coût de la sortie. Beaucoup de pêcheurs empruntent pour remplir le réservoir. Une sortie vide n'est donc pas une mauvaise journée. C'est une dette."
- body: "Et il y a le vent. En juillet 2026, deux pirogues ont chaviré en une semaine à Grand-Lahou. Personne ne prend la mer en espérant que le vent se lève."
- sources (mono, small): "Sources : Atlas des pêches artisanales d'Afrique de l'Ouest (IRD), France 24 (2024), Afrikmag (2026)."

Three stat cards, equal treatment:

| Chiffre | Légende |
|---|---|
| `2/3` | "du coût d'une sortie part dans le carburant" |
| `40 %` | "de baisse de la production halieutique ivoirienne en quelques années" |
| `160` | "caractères suffisent pour dire de rester à terre" |

### S2. Comment ça marche

- kicker: `COMMENT ÇA MARCHE`
- headline: "Trois étapes, et personne n'installe rien."
- Step 1: "Le satellite mesure" / "Chlorophylle, température de surface, vent. Trois mesures publiques, prises au-dessus de votre zone de sortie." **Image: 01, the instrument over the water.**
- Step 2: "Le score tranche" / "Un indice de 0 à 100 croise la richesse de l'eau et le danger du vent. Le vent fort l'emporte toujours sur le poisson." **Image: 02, the water's colour reading as data.**
- Step 3: "Le SMS part" / "Un message de 160 caractères sur un téléphone simple. Pas d'application, pas de forfait internet." **Image: 03, the phone in a hand at the water's edge at dawn.**

All three steps get an image. An unequal step reads as a hole. The self-drawing orbital
trace runs down the left margin of this section.

### S3. The one interactive moment: sondez la zone

Lives between S2 and S4. Press and hold, and the visitor performs the reading the service
performs every morning.

- kicker: `ESSAYEZ`
- headline: "Maintenez pour sonder la zone."
- subline: "C'est exactement ce que le service fait chaque matin, pour chaque pêcheur inscrit."
- While held: three gauges fill in sequence (`CHLOROPHYLLE 0,62 mg/m³`, `TEMPÉRATURE 27,4 °C`, `VENT 5,1 m/s`), the score counts up from 0 to 78, then the decision chip resolves.
- Result: chip `PARTEZ`, line "Score 78 sur 100. Eau productive, mer calme."
- hint while sounding: "Relâchez et la sonde redescend."
- hint once complete: "Zone sondée. Le pêcheur reçoit ce mot par SMS."
- Reduced motion: the final state is shown at once, no hold required.

Releasing early eases the progress back down. It never snaps. Completing it latches: the
reading is earned and it stays, which is why the hint changes at that moment.

### S4. Quand le satellite ne voit rien

- kicker: `QUAND ON NE SAIT PAS`
- headline: "Le jour où le nuage cache la mer, le service le dit."
- body: "Sous une couverture nuageuse, il n'y a pas de mesure exploitable. Le service affiche DONNÉES INDISPONIBLES et demande de réessayer le lendemain. Il n'invente pas un chiffre."
- body: "Un pêcheur qui découvre une fois qu'on lui a menti n'ouvrira plus jamais le message. C'est pour cela que le silence fait partie du service."
- chip: `DONNÉES INDISPONIBLES` in grey.

### S5. Ce que voit la coopérative

- kicker: `ESPACE COOPÉRATIVE`
- headline: "La coopérative voit sa flotte, pas seulement la météo."
- list:
  - "Le registre des pêcheurs, leur pirogue et leur zone de rattachement."
  - "Les alertes des 30 derniers jours, et lesquelles sont vraiment parties."
  - "La part de jours ÉVITEZ, qui dit combien de sorties dangereuses ont été évitées."
  - "Les 14 derniers jours en un coup d'œil, par décision."
- **Image: the ending frame of the hero film, reused as this section's design image.**

### S6. L'offre

- kicker: `L'OFFRE`
- headline: "Le pêcheur ne paie jamais. La coopérative s'abonne."
- body: "Pendant le pilote, l'accès est gratuit pour les coopératives retenues. L'État et les ONG financent cette phase pour la flotte artisanale. La facturation viendra ensuite, et elle sera annoncée avant, jamais après."
- card title: "Abonnement coopérative"
- card items: "Alertes SMS illimitées pour tous les membres" / "Tableau de bord cartographique en temps réel" / "Registre des pêcheurs et suivi des sorties"
- card note: "Tarif annoncé à la fin du pilote."

### S7. Les questions qu'on nous pose

- Q: "Mes pêcheurs n'ont pas de smartphone."
  A: "Tant mieux. Le service envoie un SMS de 160 caractères, lisible sur le téléphone le plus simple. Rien à installer, aucun forfait internet à payer."
- Q: "Est-ce que vous savez vraiment où est le poisson ?"
  A: "Non, et nous ne le dirons jamais. Le service mesure la richesse de l'eau, qui indique où le poisson vient se nourrir. C'est un indicateur, pas une promesse de prise. Les seuils sont calibrés avec des experts et affichés tels quels."
- Q: "Et si le satellite ne voit rien ?"
  A: "Le message dit DONNÉES INDISPONIBLES. Le service préfère se taire plutôt qu'inventer un chiffre."
- Q: "Pourquoi le vent compte autant que le poisson ?"
  A: "Parce qu'une pirogue qui ne rentre pas coûte plus cher qu'une sortie vide. Au-delà de 10 mètres par seconde, la décision passe à ÉVITEZ, quelle que soit la richesse de l'eau."
- Q: "Sur quelle zone ça marche ?"
  A: "La côte ivoirienne, d'Abidjan à Grand-Lahou, San Pédro et Sassandra. Chaque coopérative déclare ses zones de sortie."
- Q: "Qui paie les SMS ?"
  A: "La coopérative, dans son abonnement. Le pêcheur ne paie ni le message ni l'inscription."

### S8. The single call to action and the form

- id: `#inscription`
- kicker: `INSCRIRE MA COOPÉRATIVE`
- headline: "Dites-nous où sortent vos pirogues."
- subline: "Nous ouvrons le pilote coopérative par coopérative. Laissez votre zone et votre contact, la réponse arrive sous 48 heures."
- Fields: "Nom de la coopérative" / "Votre nom" / "Téléphone ou email" / "Zone de sortie principale" / "Nombre de pêcheurs"
- Button: "Envoyer la demande"
- Success: "C'est enregistré. Nous revenons vers vous sous 48 heures."
- Handling: to be settled with the owner before build completion. Real leads mean mailto or
  a form service, never a silent success state. Whatever is chosen, the page says plainly
  where the message lands.

### Footer

- brand line: "Pêche-Sat CI. Le satellite regarde la mer. Vous décidez."
- data line: "Données publiques MODIS-Aqua (NASA), NOAA OISST, NOAA GFS."
- **AI disclosure: "Les images et le film de ce site sont générés par intelligence artificielle. Le service, les données satellite et les calculs sont réels."**
- nav links, year.

---

## 7. The vector layer plan

Every element drawn by hand in SVG. All of it honours reduced motion: final state shown,
drives stopped.

- **La trace orbitale.** A dotted arc down the left margin of S2 that draws itself on scroll
  via `stroke-dashoffset`, with a node at each of the three steps.
- **La rampe chlorophylle.** A hand built gradient bar (indigo, cyan, jade, amber) used as
  the divider between sections and as the gauge fill in the interactive moment. It is the
  false colour ramp of ocean colour imagery, which is this brand's own material world.
- **Le graticule.** A faint latitude and longitude grid in the fixed background environment
  layer, drifting on a 90 second cycle so scrolling feels like moving through one place.
- **Les motes.** Plankton scale particles in the background layer, whisper level, 60 second
  cycles with negative delays so they are mid cycle at first paint.
- **La puce de décision.** The chip component: mono label, 1px border, the decision colour.
  The site's punctuation, used in the hero HUD, the interactive moment, S4, and S5.
- **L'onde.** One living element per section at whisper level: a slow horizontal swell line
  that breathes under each section kicker.

---

## 8. The engineering list

Nothing here is optional. Full detail in `references/scrub-pipeline.md`.

- Video fetched as a Blob, streamed behind an honest loading ring, poster painted first.
- Byte size hardcoded as the Content-Length fallback, 20 second watchdog, abort into the
  still hero.
- dt normalized lerp in a rAF loop that rests when converged and when the hero is off screen.
- Gated seeks with newest target coalescing and the error handler that breaks the deadlock.
- Delta gated DOM writes for every band, chip, and readout. 10Hz cap on the HUD text.
- Band pacing in vh, validated by the flick test at 120, 240 and 360px steps.
- The four layer legibility system: global scrim, per band scrim riding `--k`, the three
  layer text shadow token, chip scrims for HUD text. Worst frame audit at 3.5:1 minimum.
- The five static hero gates, identical strings in CSS and JS, armed and disarmed live from
  `change` listeners.
- Complete without the video: every band, section, and the CTA work over the poster.
- Reduced motion honoured live in both directions, with pins undone on the way back.
- `overflow-x: clip` on html and body, `hidden` declared first.
- The quality floor in full: semantic landmarks, skip link, 4.5:1 body contrast, focus
  visible in the accent, 44px touch targets, inline SVG favicon, og tags patched at deploy.

---

## 9. The copy gate

Every viewer facing line above ships verbatim. Before anyone sees the built page it must
pass the Phase 9 gate: zero em dashes, zero stock words, and the body copy sweep for AI
tells. The designed devices in this package stay: the staccato pair in band 3 ("La couleur
de l'eau dit où est le poisson." / "Le vent dit si vous rentrerez.") and the closing line
of S1 ("C'est une dette.") are deliberate, not drift.
