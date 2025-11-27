import React from 'react';
import '../assets/accueil.css'; // Make sure this path is correct relative to your file structure

const Accueil = () => {
    return (
        <div className="accueil-container">
            <div className="accueil-card">
                <h1 className="accueil-title">Planning Poker</h1>
                <p>Bienvenue sur votre application d'estimation agile.</p>
                <p>Rejoignez une table ou créez une nouvelle session.</p>
                <button className="accueil-button">Commencer une partie</button>
            </div>
        </div>
    );
};

export default Accueil;
