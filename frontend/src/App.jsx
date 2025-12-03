import { useState } from 'react'
import './assets/App.css'
import { BrowserRouter, Routes, Route } from 'react-router-dom'
import Header from "./layout/header";
import Accueil from './pages/accueil.jsx'
import AccueilUser from './pages/accueiluser.jsx'


function App() {
  const [count, setCount] = useState(0)

  return (
    <BrowserRouter>
      <Header />
      <Routes>
        <Route path="/" element={<Accueil />} />
        <Route path="/accueil" element={<Accueil />} />
        <Route path="/accueiluser" element={<AccueilUser />} />

      </Routes>
    </BrowserRouter>
  )
}

export default App
