import React, { useState, useEffect, useCallback } from 'react';
import { useParams, useLocation } from 'react-router-dom';
import { 
    Box, Container, Typography, Stack, Button, Card, CardContent, 
    Divider, Grid, Paper, Tooltip, Chip 
} from '@mui/material';
import CheckCircleOutlineIcon from '@mui/icons-material/CheckCircleOutline';
import VisibilityIcon from '@mui/icons-material/Visibility';
import VisibilityOffIcon from '@mui/icons-material/VisibilityOff';
import RefreshIcon from '@mui/icons-material/Refresh';
//import { getCardSet, getCardSvg } from '../services/card'; 
// Importation des fonctions API
import { fetchSessions } from '../services/api'
import { getCardSet, getCardSvg } from '../services/card';

// --- STYLES ---
const componentStyles = {
    storyCard: {
        minHeight: '200px',
        p: 3,
        textAlign: 'center',
        background: '#f8f8ff', // Couleur douce pour la story
    },
    cardContainer: {
        display: 'flex',
        justifyContent: 'center',
        alignItems: 'center',
        height: '100%',
        cursor: 'pointer',
        transition: 'transform 0.1s, box-shadow 0.1s',
        '&:hover': {
            transform: 'translateY(-5px)',
            boxShadow: '0 4px 12px rgba(0,0,0,0.1)',
        },
    },
    selectedCard: {
        border: '3px solid',
        borderColor: 'primary.main',
        transform: 'scale(1.05)',
        boxShadow: '0 4px 15px rgba(0, 0, 0, 0.2)',
    },
    svgStyle: {
        width: '100%',
        height: 'auto',
        maxWidth: '80px', // Taille maximale pour les cartes
    }
};

// --- LOGIQUE DU COMPOSANT ---

export default function GameSession() {
    const { id_session } = useParams();
    const location = useLocation();
    
    // 1. Récupération du mode de jeu depuis l'URL (ex: /partie/123456?mode=strict)
    const queryParams = new URLSearchParams(location.search);
    const gameMode = queryParams.get('mode') || 'strict';

    // 2. État du jeu
    const [currentStory, setCurrentStory] = useState(null); // Story en cours
    const [selectedCard, setSelectedCard] = useState(null); // Carte sélectionnée par l'utilisateur
    const [votes, setVotes] = useState({}); // Votes des autres joueurs (temps réel simulé)
    const [showVotes, setShowVotes] = useState(false); // État de révélation des votes
    const [loading, setLoading] = useState(true);

    // 3. Jeux de cartes selon les consignes (Fibonacci + Spéciaux)
    const cardSet = getCardSet(gameMode);
    
    // 4. SIMULATION de récupération de session
    const fetchSessionData = useCallback(async () => {
        setLoading(true);
        // 🚨 REMPLACER PAR VOTRE VÉRITABLE APPEL API 
        // Ex: fetch(`/api/sessions/${id_session}/current_story`)
        await new Promise(r => setTimeout(r, 800)); 
        
        // Données simulées
        setCurrentStory({
            id: 1,
            titre: "Implémenter la page de sélection du mode de jeu.",
            contenu: "Créer le composant React 'ModeSelection' pour permettre à l'utilisateur de choisir entre Stricte, Moyenne, Médiane, etc., et d'importer le JSON des stories.",
            valeur: null, // Valeur finale de la story
        });
        setVotes({
            "Alice": "5",
            "Bob": "8",
            "Charlie": "5",
            "David": null, // N'a pas encore voté
        });
        setLoading(false);
    }, [id_session]);

    useEffect(() => {
        fetchSessionData();
    }, [fetchSessionData]);
    
    // 5. Handlers
    
    const handleCardClick = (value) => {
        // Logique d'envoi du vote via WebSocket (omise ici)
        setSelectedCard(value);
        console.log(`Vote envoyé pour la carte: ${value}`);
    };

    const handleRevealVotes = () => {
        // Logique pour envoyer la commande de révélation au serveur
        setShowVotes(true);
    };

    if (loading) {
        return <Container maxWidth="md" sx={{ py: 6 }}><Typography align="center">Chargement de la session...</Typography></Container>;
    }

    return (
        <Container maxWidth="lg" sx={{ py: 4 }}>
            <Stack spacing={3}>
                <Box>
                    <Typography variant="h5" fontWeight={700}>
                        Session : {id_session} 
                        <Chip label={gameMode.toUpperCase()} color="secondary" size="small" sx={{ ml: 2 }} />
                    </Typography>
                    <Typography variant="body2" color="text.secondary">
                        Vous votez pour : **{currentStory?.titre}**
                    </Typography>
                </Box>
                <Divider />

                {/* 1. Zone de la User Story en cours */}
                <Card variant="outlined" sx={componentStyles.storyCard}>
                    <CardContent>
                        <Typography variant="h6" color="text.primary" gutterBottom>
                            {currentStory?.titre}
                        </Typography>
                        <Typography variant="body1" color="text.secondary">
                            {currentStory?.contenu}
                        </Typography>
                        <Stack direction="row" spacing={2} justifyContent="center" mt={3}>
                            <Button 
                                variant="contained" 
                                color={showVotes ? "error" : "primary"}
                                onClick={handleRevealVotes}
                                startIcon={showVotes ? <VisibilityOffIcon /> : <VisibilityIcon />}
                                disabled={showVotes} // Désactiver si déjà révélé
                            >
                                {showVotes ? "Votes Révélés" : "Révéler les votes"}
                            </Button>
                            {showVotes && (
                                <Button 
                                    variant="outlined" 
                                    startIcon={<RefreshIcon />}
                                    // 🚨 Logique pour passer à la story suivante ou lancer un nouveau vote
                                >
                                    Nouveau Vote / Story Suivante
                                </Button>
                            )}
                        </Stack>
                    </CardContent>
                </Card>

                {/* 2. Affichage des joueurs et des votes */}
                <Box>
                    <Typography variant="subtitle1" fontWeight={600} mb={1}>
                        Joueurs ({Object.keys(votes).length + 1} en ligne)
                    </Typography>
                    <Grid container spacing={2}>
                        {/* Carte de l'utilisateur actuel */}
                        <Grid item xs={6} sm={3}>
                            <Paper elevation={3} sx={{ p: 1.5, textAlign: 'center' }}>
                                <Typography variant="subtitle2" sx={{ fontWeight: 700 }}>Moi (dd)</Typography>
                                {selectedCard ? (
                                    <Chip label="Voté" color="success" size="small" icon={<CheckCircleOutlineIcon />} sx={{ mt: 1 }} />
                                ) : (
                                    <Chip label="En attente" color="default" size="small" sx={{ mt: 1 }} />
                                )}
                            </Paper>
                        </Grid>
                        {/* Cartes des autres joueurs */}
                        {Object.entries(votes).map(([player, voteValue]) => (
                            <Grid item xs={6} sm={3} key={player}>
                                <Paper elevation={2} sx={{ p: 1.5, textAlign: 'center' }}>
                                    <Typography variant="subtitle2">{player}</Typography>
                                    {showVotes ? (
                                        <Typography variant="h5" sx={{ mt: 1 }}>
                                            {voteValue !== null ? voteValue : '🤷'}
                                        </Typography>
                                    ) : (
                                        <Chip label={voteValue ? "Voté" : "En attente"} color={voteValue ? "primary" : "default"} size="small" sx={{ mt: 1 }} />
                                    )}
                                </Paper>
                            </Grid>
                        ))}
                    </Grid>
                </Box>
                
                <Divider />

                {/* 3. Zone de sélection des cartes de vote */}
                <Box>
                    <Typography variant="h6" fontWeight={600} mb={2}>
                        Sélectionnez votre estimation :
                    </Typography>
                    <Grid container spacing={2} justifyContent="center">
                        {cardSet.map(value => (
                            <Grid item key={value} xs={3} sm={2} md={1}>
                                <Paper
                                    elevation={selectedCard === value ? 8 : 2}
                                    onClick={() => handleCardClick(value)}
                                    sx={{ 
                                        ...componentStyles.cardContainer,
                                        ...(selectedCard === value && componentStyles.selectedCard),
                                    }}
                                >
                                    <Tooltip title={`Voter ${value}`} placement="top">
                                        <Box sx={componentStyles.svgStyle}>
                                            {/* Rendu du SVG (via la fonction utilitaire) */}
                                            {getCardSvg(value)}
                                        </Box>
                                    </Tooltip>
                                </Paper>
                            </Grid>
                        ))}
                    </Grid>
                </Box>
            </Stack>
        </Container>
    );
}