// src/utils/cardUtils.js
import React from 'react';
import Card0 from '../assets/cartes/cartes_0.svg?react';
import Card1 from '../assets/cartes/cartes_1.svg?react';
import Card2 from '../assets/cartes/cartes_2.svg?react';
import Card3 from '../assets/cartes/cartes_3.svg?react';
import Card5 from '../assets/cartes/cartes_5.svg?react';
import Card8 from '../assets/cartes/cartes_8.svg?react';
import Card13 from '../assets/cartes/cartes_13.svg?react';
import Card20 from '../assets/cartes/cartes_20.svg?react';
import Card40 from '../assets/cartes/cartes_40.svg?react';
import Card100 from '../assets/cartes/cartes_100.svg?react';
import CardCoffee from '../assets/cartes/cartes_cafe.svg?react';
import CardInterro from '../assets/cartes/cartes_interro.svg?react';

// Retourne l'ensemble des cartes en fonction du mode de jeu
export const getCardSet = () => {
    const FIBONACCI_SET = ['0', '1', '2', '3', '5', '8', '13', '20', '40', '100'];
    const SPECIAL_CARDS = ['coffee', '?'];
    
    return [...FIBONACCI_SET, ...SPECIAL_CARDS];
};

// Retourne le composant SVG pour la valeur de carte donnée.
export const getCardSvg = (value) => {
    const CARD_SVG_MAP = {'0': Card0, '1': Card1, '2': Card2, '3': Card3, '5': Card5, '8':Card8, '13': Card13, '20': Card20,'40': Card40,'100': Card100, 'coffee': CardCoffee,'?': CardInterro, };
    const Component = CARD_SVG_MAP[value];

    return <Component />;
};