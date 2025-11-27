import { useState } from 'react'
import './assets/App.css'
import { BrowserRouter, Routes, Route } from 'react-router-dom'
import Accueil from './pages/accueil.jsx'



function App() {
  const [count, setCount] = useState(0)

  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<Accueil />} />
        <Route path="/accueil" element={<Accueil />} />
      </Routes>
    </BrowserRouter>
  )
}

export default App
