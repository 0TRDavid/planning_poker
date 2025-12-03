// src/services/api.js

const API_BASE_URL = 'http://localhost:8000/api'; // Utilisez votre variable d'environnement ici !

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
    // Vous pouvez relancer l'erreur ou retourner un tableau vide
    return []; 
  }
};

/**
 * Crée une nouvelle session (Simulation).
 */
export const createSession = async () => {
    // Ici, vous feriez une requête POST vers votre endpoint de création
    console.log("Tentative de création de session...");
    await new Promise(r => setTimeout(r, 500)); // Simule le délai du réseau
    // Si la création est réussie, vous retourneriez les données de la nouvelle session
    return { success: true, message: "Session créée avec succès." };
};