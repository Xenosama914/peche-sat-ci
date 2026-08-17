import axios from "axios";

const API_BASE_URL = import.meta.env.VITE_API_URL || "http://localhost:8000";

const client = axios.create({ baseURL: API_BASE_URL });

export const listerPecheurs = () => client.get("/api/pecheurs").then((r) => r.data);

export const inscrirePecheur = (payload) =>
  client.post("/api/pecheurs", payload).then((r) => r.data);

export const obtenirScore = (latitude, longitude, zone) =>
  client
    .get("/api/score", { params: { latitude, longitude, zone } })
    .then((r) => r.data);

export const envoyerAlerteSms = (payload) =>
  client.post("/api/sms/alerte", payload).then((r) => r.data);

const CLE_JETON = "peche-sat-ci.jeton";

export const stockerJeton = (jeton) => localStorage.setItem(CLE_JETON, jeton);
export const supprimerJeton = () => localStorage.removeItem(CLE_JETON);
export const obtenirJeton = () => localStorage.getItem(CLE_JETON);

export const connexionCooperative = (email, motDePasse) =>
  client
    .post("/api/auth/connexion", { email, mot_de_passe: motDePasse })
    .then((r) => r.data);

export const obtenirTableauBordCooperative = () =>
  client
    .get("/api/cooperative/tableau-de-bord", {
      headers: { Authorization: `Bearer ${obtenirJeton()}` },
    })
    .then((r) => r.data);

export default client;
