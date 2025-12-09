import React, { useState, useEffect, useCallback, useRef } from 'react';
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
import { fetchSessionById, voteCard } from '../services/api'
import { getCardSet, getCardSvg } from '../services/card';


// Etapes de la partie :
// 1. Récupérer l'ensemble des infos de la session (stories, mode de jeu) via l'API grâce à l'id_session dans l'URL
// 2. Afficher la premiere story qui a une valeur = NULL (non encore votée)
// L'utilisateur vote en cliquant sur une carte
// 3. Envoyer le vote au serveur API --> voteJoueur
// 4. Interrogation régulière (polling) pour récupérer les votes des autres joueurs et savoir si tout le monde a voté
// Lorsque le back valide que tous les joueurs ont voté, on calcule la valeur mise sur la story, maj et envoi au back --> majSession 
// Afficher les votes reçus (avec une animation sympa)
// On retourne à l'étape 2 jusqu'à la fin des stories // sessions fini ? on drop la table partie et on affiche les résultats finaux


// Fais gaffe de bien drop les lignes dans la table partie si tu veux faire des test sinon tu peux pas rejoindre 2 fois !!





// ET APPAREMMENT DJANGO CHANNEL POUR LE TEMPS RÉEL MAIS PAS LE TEMPS DE L'IMPLÉMENTER LÀ MAINTENANT




// test websocket


// function Session() {
//     const [messages, setMessages] = useState([]);
//     const ws = useRef(null);

//     useEffect(() => {
//         // Connectez-vous au WebSocket
//         ws.current = new WebSocket(`ws://localhost:8000/ws/session/${id_session}/`);

//         ws.current.onopen = () => {
//             console.log('WebSocket connecté');
//         };

//         ws.current.onmessage = (event) => {
//             const data = JSON.parse(event.data);
//             setMessages(prev => [...prev, data]);
//             // Mettez à jour l'interface (votes, nouvelles histoires, etc.)
//         };

//         ws.current.onclose = () => {
//             console.log('WebSocket fermé');
//         };

//         return () => {
//             ws.current.close();
//         };
//     }, [id_session]);

//     const sendMessage = (message) => {
//         if (ws.current.readyState === WebSocket.OPEN) {
//             ws.current.send(JSON.stringify(message));
//         }
//     };

//     return (
//         <div>
//             <ul>
//                 {messages.map((msg, i) => (
//                     <li key={i}>{msg.content}</li>
//                 ))}
//             </ul>
//             <button onClick={() => sendMessage({type: 'vote', value: '5'})}>
//                 Voter
//             </button>
//         </div>
//     );
// }

// export default Session;
// fin test websocket













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
    const gameMode = queryParams.get('mode') || 'strict'; // Pas géré pour le moment
    const username = (() => {
        const match = document.cookie.match(/(?:^|;\s*)username=([^;]+)/);
        return match ? decodeURIComponent(match[1]) : null;
    })();

    // 2. État du jeu
    const [currentStory, setCurrentStory] = useState(null); // Story en cours
    const [selectedCard, setSelectedCard] = useState(null); // Carte sélectionnée par l'utilisateur
    const [votes, setVotes] = useState({}); // Votes des autres joueurs (temps réel simulé)
    const [showVotes, setShowVotes] = useState(false); // État de révélation des votes
    const [loading, setLoading] = useState(true);

    // 3. Jeux de cartes selon les consignes (Fibonacci + Spéciaux)
    const cardSet = getCardSet(gameMode);
    
    // Etape1 : récupération de session
const fetchSessionData = useCallback(async () => {
    setLoading(true);
    try {
        const data = await fetchSessionById(id_session);
        console.log("Données de la session récupérées:", data);
        
        let currentStory = data.stories && data.stories.length > 0 ? data.stories[0] : null;
        setCurrentStory(currentStory);


        await new Promise(r => setTimeout(r, 800));

        // Simuler des votes reçus (à remplacer par WebSocket ou autre logique temps réel)
        setVotes({
            "Alice": "5",
            "Bob": "8",
            "Charlie": "5",
            "David": null,
        });
    } catch (error) {
        console.error("Erreur lors de la récupération des données de la session:", error);
    } finally {
        setLoading(false);
    }
}, [id_session]);


    useEffect(() => {
        fetchSessionData();
    }, [fetchSessionData]);
    
    // 5. Handlers
    
    const handleCardClick = (value) => {
        // Logique d'envoi du vote via WebSocket (omise ici)
        setSelectedCard(value);
        voteCard(id_session, username, value);
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