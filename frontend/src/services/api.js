// src/services/api.js
const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000/api'; 

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
 * Crée une nouvelle session via l'API Django et envoie le tableau de stories.
 * @param {string} titre - Le titre de la nouvelle session.
 * @param {Array<Object>} stories - La liste des user stories au format JSON.
 * @returns {Promise<Object>} Les données de la session créée.
 */
export const createSession = async (titre, stories = []) => {
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