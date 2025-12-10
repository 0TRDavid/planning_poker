import { useState } from 'react'
import './assets/App.css'
import { BrowserRouter, Routes, Route } from 'react-router-dom'
import Header from "./layout/header";
import Accueil from './pages/accueil.jsx'
import AccueilUser from './pages/accueil_user.jsx'
import Creation_session from './pages/creation_session.jsx'
import GameSession from './pages/partie.jsx';
import Resultats from './pages/resultat.jsx';


function App() {
  const [count, setCount] = useState(0)

  return (
    <BrowserRouter>
      <Header />
      <Routes>
        <Route path="/" element={<Accueil />} />
        <Route path="/accueiluser" element={<AccueilUser />} />
        <Route path="/create-session" element={<Creation_session />} />
        <Route path="/partie/:id_session" element={<GameSession />} />
        <Route path="/partie/:id_session/resultats" element={<Resultats />} />

      </Routes>
    </BrowserRouter>
  )
}

export default App
