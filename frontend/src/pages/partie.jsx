// src/pages/partie.jsx
import React, { useState, useEffect, useCallback } from 'react';
import { useParams, useLocation, useNavigate } from 'react-router-dom'; // AJOUT useNavigate
import { Container, Stack, Box, Typography, Chip, Divider } from '@mui/material';

// Imports Logic & Services
import { fetchSessionById, voteCard, fetchVotes, closeStory } from '../services/api';
import { getCardSet } from '../services/card';

// Imports Composants
import StoryDisplay from '../components/partie/StoryDisplay';
import PlayersGrid from '../components/partie/PlayersGrid';
import VotingDeck from '../components/partie/VotingDeck';

export default function GameSession() {
    const { id_session } = useParams();
    const navigate = useNavigate(); // Hook pour la redirection
    const location = useLocation();
    
    // Récupération user/mode
    const queryParams = new URLSearchParams(location.search);
    const gameMode = queryParams.get('mode') || 'strict'; 
    const username = document.cookie.match(/(?:^|;\s*)username=([^;]+)/)?.[1] ? decodeURIComponent(document.cookie.match(/(?:^|;\s*)username=([^;]+)/)[1]) : "Anonyme";

    // --- NOUVEAUX ÉTATS ---
    const [allStories, setAllStories] = useState([]); // Liste complète
    const [storyIndex, setStoryIndex] = useState(0);  // Position actuelle
    // ----------------------

    const [selectedCard, setSelectedCard] = useState(null); 
    const [votes, setVotes] = useState({}); 
    const [showVotes, setShowVotes] = useState(false); 
    const [loading, setLoading] = useState(true);

    // Variable dérivée : la story actuelle dépend de l'index
    const currentStory = allStories[storyIndex] || null;
    const cardSet = getCardSet(gameMode);

    // --- LOGIQUE ---

    const fetchSessionData = useCallback(async () => {
        setLoading(true);
        try {
            const data = await fetchSessionById(id_session);
            // On stocke toutes les stories
            if (data.stories && Array.isArray(data.stories)) {
                setAllStories(data.stories);
            }
        } catch (error) {
            console.error("Erreur session:", error);
        } finally {
            setLoading(false);
        }
    }, [id_session]);

    const refreshGameState = async () => {
        if (!id_session) return;
        try {
            const dataPartie = await fetchVotes(id_session);
            const votesMap = {};
            if (Array.isArray(dataPartie)) {
                dataPartie.forEach(player => {
                    if (player.username !== username) {
                        votesMap[player.username] = player.carte_choisie; 
                    }
                });
            }
            setVotes(votesMap);
        } catch (error) {
            console.error("Erreur polling:", error);
        }
    };

    // --- GESTION DU BOUTON SUIVANT ---
    const handleNextStory = async () => {
        // APPEL AU BACK POUR SAUVEGARDER LE RÉSULTAT
        try {
            await closeStory(id_session, storyIndex);
            
            const nextIndex = storyIndex + 1;
            if (nextIndex < allStories.length) {
                setStoryIndex(nextIndex);
                setShowVotes(false);
                setSelectedCard(null);
                setVotes({});
            } else {
                navigate(`/partie/${id_session}/resultats`);
            }
        } catch (err) {
            console.error("Impossible de sauvegarder la story", err);
        }
    };

    // Cycles de vie
    useEffect(() => {
        fetchSessionData();
        const intervalId = setInterval(refreshGameState, 2000);
        return () => clearInterval(intervalId);
    }, [fetchSessionData]);

    // Handlers
    const handleCardClick = async (value) => {
        setSelectedCard(value);
        await voteCard(id_session, username, value);
        refreshGameState();
    };

    if (loading) return <Container sx={{ py: 6 }}><Typography align="center">Chargement...</Typography></Container>;

    return (
        <Container maxWidth="lg" sx={{ height:"90%", width:"100%", paddingTop: '80px' }}>
            <Stack spacing={4}>
                <Box>
                    <Typography variant="h5" fontWeight={700}>
                        Session : {id_session} 
                        <Chip label={gameMode} color="secondary" size="small" sx={{ ml: 2 }} />
                        <Chip label={`${storyIndex + 1} / ${allStories.length}`} size="small" sx={{ ml: 1 }} />
                    </Typography>
                </Box>
                <Divider />

                {/* ZONE 1 : STORY (avec la nouvelle prop onNext) */}
                <StoryDisplay 
                    currentStory={currentStory} 
                    showVotes={showVotes} 
                    onReveal={() => setShowVotes(true)}
                    onNext={handleNextStory} 
                />

                {/* ZONE 2 : JOUEURS */}
                <PlayersGrid 
                    votes={votes} 
                    username={username} 
                    hasVoted={!!selectedCard} 
                    showVotes={showVotes} 
                />
                
                <Divider />

                {/* ZONE 3 : DECK */}
                <VotingDeck 
                    cardSet={cardSet} 
                    selectedCard={selectedCard} 
                    onVote={handleCardClick} 
                />
            </Stack>
        </Container>
    );
}