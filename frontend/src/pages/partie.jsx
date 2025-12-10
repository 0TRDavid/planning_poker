import React, { useState, useEffect, useCallback } from 'react';
import { useParams, useLocation } from 'react-router-dom';
import { Container, Stack, Box, Typography, Chip, Divider } from '@mui/material';

// Imports Logic & Services
import { fetchSessionById, voteCard, fetchVotes } from '../services/api';
import { getCardSet } from '../services/card';

// Imports Composants (Ajuste le chemin si besoin)
import StoryDisplay from '../components/partie/StoryDisplay';
import PlayersGrid from '../components/partie/PlayersGrid';
import VotingDeck from '../components/partie/VotingDeck';

export default function GameSession() {
    // --- 1. HOOKS & STATE ---
    const { id_session } = useParams();
    const location = useLocation();
    
    // Récupération user/mode
    const queryParams = new URLSearchParams(location.search);
    const gameMode = queryParams.get('mode') || 'strict'; 
    const username = document.cookie.match(/(?:^|;\s*)username=([^;]+)/)?.[1] ? decodeURIComponent(document.cookie.match(/(?:^|;\s*)username=([^;]+)/)[1]) : "Anonyme";

    const [currentStory, setCurrentStory] = useState(null); 
    const [selectedCard, setSelectedCard] = useState(null); 
    const [votes, setVotes] = useState({}); 
    const [showVotes, setShowVotes] = useState(false); 
    const [loading, setLoading] = useState(true);

    const cardSet = getCardSet(gameMode);

    // --- 2. LOGIQUE (Polling & Fetch) ---
    const fetchSessionData = useCallback(async () => {
        setLoading(true);
        try {
            const data = await fetchSessionById(id_session);
            // Logique simplifiée : prend la 1ère story
            setCurrentStory(data?.stories?.[0] || null);
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

    // Cycles de vie
    useEffect(() => {
        fetchSessionData();
        const intervalId = setInterval(refreshGameState, 2000);
        return () => clearInterval(intervalId);
    }, [fetchSessionData]);

    // --- 3. HANDLERS ---
    const handleCardClick = (value) => {
        setSelectedCard(value);
        voteCard(id_session, username, value);
        refreshGameState();
    };

    // --- 4. RENDER ---
    if (loading) return <Container sx={{ py: 6 }}><Typography align="center">Chargement...</Typography></Container>;

    return (
        <Container maxWidth="lg" sx={{ height:"100%", width:"100%", paddingTop: '85px' }}>
            <Stack spacing={2}>
                {/* En-tête simple */}
                <Box>
                    <Typography variant="h5" fontWeight={700}>
                        Session : {id_session} 
                        <Chip label={gameMode} color="secondary" size="small" sx={{ ml: 2 }} />
                    </Typography>
                </Box>
                <Divider />

                {/* ZONE 1 : STORY */}
                <StoryDisplay 
                    currentStory={currentStory} 
                    showVotes={showVotes} 
                    onReveal={() => setShowVotes(true)} 
                />
                <Divider />

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