import React, { useState, useEffect } from 'react';
import { Container, Typography, Paper, Button, Stack } from '@mui/material';
import { useParams } from 'react-router-dom';
import DownloadIcon from '@mui/icons-material/Download';
import HomeIcon from '@mui/icons-material/Home';
import { fetchSessionById } from '../services/api'; // On réutilise ton service

export default function Resultats() {
    const { id_session } = useParams();
    const [sessionData, setSessionData] = useState(null);

    // 1. On récupère les données finales de la session au chargement
    useEffect(() => {
        const loadData = async () => {
            if (id_session) {
                const data = await fetchSessionById(id_session);
                setSessionData(data);
            }
        };
        loadData();
    }, [id_session]);

    // 2. Fonction pour déclencher le téléchargement du JSON
    const handleDownload = () => {
        if (!sessionData) return;

        // Création du fichier JSON en mémoire
        const jsonString = JSON.stringify(sessionData, null, 2);
        const blob = new Blob([jsonString], { type: "application/json" });
        const href = URL.createObjectURL(blob);

        // Création d'un lien invisible pour cliquer dessus
        const link = document.createElement('a');
        link.href = href;
        link.download = `resultats_session_${id_session}.json`;
        document.body.appendChild(link);
        link.click();
        
        // Nettoyage
        document.body.removeChild(link);
        URL.revokeObjectURL(href);
    };

    return (
        <Container maxWidth="sm" sx={{ paddingTop: '100px', minHeight: '80vh', display: 'flex', alignItems: 'center', justifyContent: 'center' }}>
            <Paper elevation={3} sx={{ p: 4, textAlign: 'center' }}>
                <Typography variant="h4" color="primary" gutterBottom>
                    Planning Poker terminé !
                </Typography>
                <Typography variant="body1"> 
                    Toutes les user stories de la session <strong>{id_session}</strong> ont été votées.
                </Typography>

                {/* Stack gère l'empilement vertical automatiquement */}
                <Stack spacing={2} mt={4} direction="column">
                    <Button 
                        variant="outlined" 
                        onClick={handleDownload}
                        startIcon={<DownloadIcon />}
                        disabled={!sessionData} // Désactivé tant que les données ne sont pas chargées
                        fullWidth
                    >
                        Télécharger les résultats (JSON)
                    </Button>

                    <Button 
                        variant="contained" 
                        href="/accueiluser"
                        startIcon={<HomeIcon />}
                        fullWidth
                    >
                        Retour à l'accueil
                    </Button>
                </Stack>
            </Paper>
        </Container>
    );
}