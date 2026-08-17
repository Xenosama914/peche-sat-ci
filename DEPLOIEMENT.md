# Mettre Pêche-Sat CI en ligne, gratuitement

Trois morceaux à héberger, et un quatrième qui existe déjà.

| Morceau | Où | Coût |
|---|---|---|
| La base de données | Neon, déjà en place | gratuit |
| Le moteur (FastAPI) | Render, service web gratuit (512 Mo, 0,1 CPU) | gratuit |
| Le tableau de bord (React) | Render, site statique | gratuit |
| La vitrine (HTML) | Render, site statique | gratuit |
| L'envoi matinal | GitHub Actions, tâche planifiée | gratuit |

**Le seul poste payant reste le SMS réel.** Africa's Talking est en mode bac à sable :
les messages partent vers un simulateur. Le jour où de vrais pêcheurs doivent recevoir
de vrais SMS, il faut un compte Africa's Talking approvisionné et un expéditeur validé.
Tout le reste de la chaîne fonctionne déjà.

---

## Étape 1 : le dépôt

Le projet doit vivre dans son propre dépôt GitHub, séparé de votre dossier utilisateur.
Le dépôt local est déjà prêt. Il reste à créer le dépôt sur GitHub (privé de préférence)
et à y envoyer le code.

Ce qui n'y montera jamais, garanti par le `.gitignore` : le fichier `.env`, la clé
`ee-key.json`, le dossier `review/` et les environnements Python et Node.

## Étape 2 : le moteur sur Render

1. Sur [render.com](https://render.com), créez un compte et reliez GitHub.
2. **New > Blueprint**, choisissez le dépôt. Render lit `render.yaml` et propose les
   trois services d'un coup.
3. Render demande les valeurs secrètes. Elles se trouvent dans votre `backend/.env` :

   | Variable | Ce que vous collez |
   |---|---|
   | `DATABASE_URL` | la chaîne de connexion Neon |
   | `JWT_SECRET` | la même qu'en local |
   | `CRON_SECRET` | la même qu'en local |
   | `GEE_SERVICE_ACCOUNT` | l'email du compte de service Google |
   | `GEE_KEY_JSON` | **le contenu entier** du fichier `ee-key.json`, pas son chemin |
   | `AT_USERNAME`, `AT_API_KEY`, `AT_SENDER_ID` | vos identifiants Africa's Talking |
   | `ORIGINES_AUTORISEES` | les adresses des deux sites, séparées par une virgule |

   `GEE_KEY_JSON` est le point qui surprend : en local le code lit un fichier, en ligne
   il lit cette variable et réécrit le fichier lui-même au démarrage.

4. Une fois le moteur en ligne, vérifiez `https://VOTRE-MOTEUR.onrender.com/api/sante`.
   Il doit répondre `{"statut":"ok"}`.

## Étape 3 : relier les deux sites au moteur

- **Tableau de bord** : la variable `VITE_API_URL` doit contenir l'adresse du moteur.
- **Vitrine** : dans `site/index.html`, la ligne `var API_BASE = '';` reçoit cette même
  adresse. Sans elle, les demandes d'inscription partent seulement par email.
- **Moteur** : `ORIGINES_AUTORISEES` doit contenir les adresses des deux sites, sinon le
  navigateur bloquera les appels. C'est une protection, pas un bug.

## Étape 4 : l'envoi matinal

Dans le dépôt GitHub, **Settings > Secrets and variables > Actions**, ajoutez :

- `API_URL` : l'adresse du moteur, sans barre oblique finale.
- `CRON_SECRET` : exactement la même valeur que côté Render.

La tâche `.github/workflows/envoi-matinal.yml` se déclenche à 05:30, heure d'Abidjan.
Elle réveille d'abord le moteur, qui dort sur un hébergement gratuit, puis lance l'envoi.
Vous pouvez aussi la lancer à la main depuis l'onglet **Actions**, bouton **Run workflow**,
ce qui est la meilleure façon de la tester le premier jour.

## Ce qu'il faut savoir sur le gratuit

- **Le moteur s'endort** après quinze minutes sans visite. Le premier appel qui le
  réveille prend jusqu'à une minute. C'est pour cela que la tâche matinale frappe deux
  fois : une fois pour réveiller, une fois pour agir.
- **Un pêcheur ne reçoit jamais deux messages le même matin.** Le moteur vérifie ce qui
  est déjà parti dans la journée avant d'envoyer.
- **Une zone en panne n'arrête pas les autres.** Si le satellite ne répond pas pour
  Sassandra, les pêcheurs de Jacqueville reçoivent quand même leur mot.
- **Pour un essai sans envoyer aucun SMS** : ajoutez `?simulation=true` à l'appel. Le
  moteur calcule tout, prépare les messages, et n'envoie rien.
