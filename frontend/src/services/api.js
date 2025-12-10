// src/services/api.js
const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000/api'; 
import axios from "axios";  
/**
 * Récupère la liste des sessions existantes depuis le backend.
 * @returns {Promise<Array>} Liste des sessions.
 */
export const fetchSessions = async () => {
  try {
    const response = await fetch(`${API_BASE_URL}/sessions/`);
    if (!response.ok) {
      throw new Error(`Erreur HTTP: ${response.status}`);
    }
    const sessions = await response.json();
    console.log("Sessions récupérées:", sessions);
    return sessions;
  } catch (error) {
    console.error("Erreur lors de la récupération des sessions:", error);
    return []; 
  }
};

/**
 * Envoi les infos de l'utilisateur pour rejoindre une partie avec son code session (alimente la table partie)
 */
 

export const joinPartie = async (id_session, username) => {
  
          const res = await fetch('/api/joinPartie/', {
            method: 'POST',
            
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ id_session, username}),
          });
          if (!res.ok) throw new Error('Failed to join');
          res
          return res.json().catch(() => null);
        };
/**
 * Crée une nouvelle session via l'API Django et envoie le tableau de stories.
 * @param {string} titre - Le titre de la nouvelle session.
 * @param {Array<Object>} stories - La liste des user stories au format JSON.
 * @param {string} mode_de_jeu - Le mode de jeu sélectionné.
 * @returns {Promise<Object>} Les données de la session créée.
 */
export const createSession = async (titre, stories = [], mode_de_jeu) => {
    try {
        const response = await fetch(`${API_BASE_URL}/sessions/`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                // Ajoutez un jeton CSRF ou d'authentification ici si nécessaire
            },
            body: JSON.stringify({
                titre: titre,
                stories: stories, // <--- C'EST ICI QUE LE TABLEAU COMPLET DOIT ÊTRE ENVOYÉ
                mode_de_jeu: mode_de_jeu,
            }),
        });

        if (!response.ok) {
            const errorData = await response.json();
            console.error("Erreur lors de la création:", errorData);
            throw new Error(`Erreur lors de la création de la session: ${response.status} - ${JSON.stringify(errorData)}`);
        }

        const newSession = await response.json();
        return newSession;

    } catch (error) {
        console.error("Échec de la création de session:", error);
        throw error;
    }
};

// Récupérer une seule session par son ID
export const fetchSessionById = async (id_session) => {
  try {
    const response = await fetch(`${API_BASE_URL}/sessions/${id_session}/`);
    if (!response.ok) {
      throw new Error(`Erreur HTTP: ${response.status}`);
    }
    const session = await response.json();
    return session;
  } catch (error) {
    console.error("Erreur lors de la récupération de la session:", error);
    return null;
  }
};

// API de la partie (voter, récupérer les votes, etc.) avec axios ou pas 
export const voteCard = async (id_session, username, carte_choisie) => {
  try {
    const response = await axios.post('/api/vote/', { id_session, username, carte_choisie });
    return response.data;
  } catch (error) {
    console.error("Erreur lors du vote:", error);
    throw error;
  } 
};

// Récupérer les votes pour une session donnée
export const fetchVotes = async (id_session) => {
  try {
    // On appelle l'endpoint 'parties' avec le filtre id_session
    const response = await axios.get(`${API_BASE_URL}/parties/`, { 
        params: { id_session: id_session } 
    });
    return response.data;
  } catch (error) {
    console.error("Erreur lors de la récupération des votes:", error);
    return []; // Retourne un tableau vide en cas d'erreur pour ne pas casser le front
  }
};

// Vérifier si tous les utilisateurs ont voté
export const checkAllVoted = async (id_session) => {
  try {
    const response = await axios.get('/api/check_all_voted/', { params: { id_session } });
    return response.data.all_voted;
  } catch (error) {
    console.error("Erreur lors de la vérification des votes:", error);
    throw error;
  }
};

// Mettre fin à une story
export const endStory = async (id_session) => {
  try {
    const response = await axios.post('/api/end_story/', { id_session });
    return response.data;
  } catch (error) {
    console.error("Erreur lors de la fin de l'histoire:", error);
    throw error;
  }
};

// src/services/api.js
export const closeStory = async (id_session, storyIndex, finalValue) => {
  try {
    const response = await fetch(`${API_BASE_URL}/sessions/${id_session}/close_story/`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ 
          story_index: storyIndex,
          final_value: finalValue // <--- Envoi au back
      }),
    });
    if (!response.ok) throw new Error('Erreur fermeture story');
    return await response.json();
  } catch (error) {
    console.error("Erreur closeStory:", error);
    throw error;
  }
};