import React, { useState, useEffect } from "react";
import Navbar from "react-bootstrap/Navbar";
import Nav from "react-bootstrap/Nav";
import "../assets/header.css"; 

function Header() {
  const [sidebarOpen] = useState(false);
  const [isFrench, setIsFrench] = useState(true); // État pour gérer la langue

  useEffect(() => {
    // Alterner la langue toutes les 30 secondes
    const interval = setInterval(() => {
      setIsFrench(prev => !prev); // Alterne entre true (français) et false (anglais)
    }, 30000); // 30 secondes

    // Nettoyage de l'intervalle lorsque le composant est démonté
    return () => clearInterval(interval);
  }, []);

  return (
    <Navbar expand="lg" className="navbar">
      <div className="navbar-container">
        {/* Bloc gauche */}
        <Nav className="d-flex align-items-center">
          <img
            src="/logo.svg"
            alt="Logo"
            style={{
              width: "50px",
              height: "75px",
              marginRight: "10px",
              marginLeft: "5px",
            }}
          />
          <Navbar.Brand className="navbar-brand">Planning Poker</Navbar.Brand>
        </Nav>

        {/* Bloc droit */}
        <Nav className="d-flex align-items-center">
          <Navbar.Brand
            className="navbar-brand2"
            rel="noopener noreferrer"
            style={{ cursor: "pointer" }}
          >
            {isFrench
              ? "Une application créée et développée par Nico & David"
              : "A solution designed and developed by Nico & David"}
          </Navbar.Brand>
        </Nav>
      </div>
    </Navbar>
  );
}

export default Header;