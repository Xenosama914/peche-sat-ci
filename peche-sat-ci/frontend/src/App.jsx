import { useState } from "react";

import Layout from "./components/Layout";
import Cooperative from "./pages/Cooperative";
import EspaceCooperative from "./pages/EspaceCooperative";
import Pecheurs from "./pages/Pecheurs";
import TableauDeBord from "./pages/TableauDeBord";

export default function App() {
  const [page, setPage] = useState("tableau-de-bord");
  const [score, setScore] = useState(null);

  return (
    <Layout page={page} onNavigate={setPage}>
      {page === "tableau-de-bord" && <TableauDeBord score={score} onScore={setScore} />}
      {page === "pecheurs" && <Pecheurs score={score} />}
      {page === "offre" && <Cooperative />}
      {page === "espace-cooperative" && <EspaceCooperative />}
    </Layout>
  );
}
