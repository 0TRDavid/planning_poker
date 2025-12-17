import React, { useState, useEffect } from 'react';
import {Box, Container, Typography, Stack, Button, TextField, Card, CardContent, Divider, CircularProgress, Chip} from '@mui/material';
import PlayArrowIcon from '@mui/icons-material/PlayArrow';
import AddIcon from '@mui/icons-material/Add';
import RefreshIcon from '@mui/icons-material/Refresh';

// Importation des fonctions API
import { fetchSessions, joinPartie } from '../services/api';
// --- STYLES (Utilisation de l'approche SX de MUI pour la cohésion) ---
const componentStyles = {
    refreshButton: {
        display: { xs: 'none', sm: 'inline-flex' }
    },
    sessionCard: {
        borderRadius: 3, 
        '&:hover': { 
            boxShadow: 3 
        }
    },
    storyBox: {
        border: '2px solid',
        borderColor: 'grey.300',
        p: 1,
        borderRadius: 1
    }
};

// --- LOGIQUE DU COMPOSANT ---

export default function AccueilUser() {
  const [sessions, setSessions] = useState([]);
  const [loading, setLoading] = useState(false);
  const [joinCode, setJoinCode] = useState('');
  const [creating, setCreating] = useState(false);


// Appel l'API pour récupérer les sessions de la bdd
  const loadSessions = async () => {
    setLoading(true);
    try {
      const data = await fetchSessions();
      setSessions(data);
    } finally {
      setLoading(false);
    }
  };

// Renvoi vers la page de création de session
  const handleCreate = async () => {
    setCreating(true);
    try {
        window.location.href = '/create-session';
    } catch (e) {
        alert("Erreur lors de la création.");
    }
  };

  // Appel l'API pour envoyer le code session et le username puis redirige vers la page partie
  const handleJoin = async () => {
    if (!joinCode.trim()) return;
    // Envoi a l'api partie l'id_session et le username (depuis cookie)
    const username = document.cookie
      .split('; ')
      .find((c) => c.startsWith('username='))
      ?.split('=')[1];
    if (!username) {
      console.warn('Username cookie not found');
    } else {
      try {
        const res = await joinPartie(joinCode, username);

        if (res?.status === 'closed') {
          console.log('Session closed, redirecting to results');
          window.location.href = `/partie/${joinCode}/resultats`;
          return; // si tu mets pas de return ici, il continue et ouvre la page partie...
        } else {
          const gameMode = res?.mode_de_jeu || 'strict';
          window.location.href = `/partie/${joinCode}?mode=${gameMode}`; // + gamemode !!
        }
        // Ouvre la page partie
      //window.location.href = `/partie/${joinCode}`;
      } catch (err) {
        console.error('Failed to join session', err);
      }
    }
    setJoinCode('');
  };
  
 // Charge les sessions au montage du composant (grace au fetchSessions plus haut)
  useEffect(() => {
    loadSessions(); 
  }, []);

    // --- FONCTION DE RENDU SECONDAIRE (Pour un code plus clair) ---
  const getStatusChip = (status) => {
      const map = {
          'open': { label: 'Ouverte', color: 'success' },
          'in_progress': { label: 'En cours', color: 'warning' },
          'closed': { label: 'Terminée', color: 'default' },
      };
      const { label, color } = map[status] || map['closed'];
      return <Chip size="small" label={label} color={color} />;
  };
  // --- RENDER DU COMPOSANT ---
  return (
    
    <Container maxWidth="md" sx={{ py: 6, paddingTop: '85px' }}>
      <Stack spacing={4}>
        <Box sx={componentStyles.headerBox}>
          <Typography variant="h4" fontWeight={600}>
            Planning Poker
          </Typography>
          <Typography variant="body1" color="text.secondary">
            Gérez vos sessions et rejoignez une estimation.
          </Typography>
        </Box>

        {/* 1. Rejoindre une session */}
        <Card variant="outlined">
          <CardContent>
            <Stack spacing={2}>
              <Typography variant="h6">Rejoindre une session</Typography>
              <Stack direction={{ xs: 'column', sm: 'row' }} spacing={2}>
                <TextField
                  label="Code session"
                  value={joinCode}
                  onChange={e => setJoinCode(e.target.value.toUpperCase())}
                  sx={{ flex: 1 }}
                />
                <Button
                  variant="contained"
                  onClick={handleJoin}
                  startIcon={<PlayArrowIcon />}
                  disabled={!joinCode.trim()}
                >
                  Rejoindre
                </Button>
              </Stack>
            </Stack>
          </CardContent>
        </Card>

        {/* 2. Affichage des sessions de l'utilisateur */}
        <Card variant="outlined">
          <CardContent>
            <Stack direction="row" justifyContent="space-between" alignItems="center" mb={1}>
              <Typography variant="h6">Mes sessions</Typography>
              <Stack direction="row" spacing={1}>
                <Button
                  size="small"
                  variant="outlined"
                  onClick={loadSessions}
                  startIcon={<RefreshIcon />}
                  disabled={loading}
                  sx={componentStyles.refreshButton}
                >
                  Rafraîchir
                </Button>
                <Button
                  size="small"
                  variant="contained"
                  onClick={handleCreate}
                  startIcon={<AddIcon />}
                  disabled={creating}
                >
                  Nouvelle
                </Button>
              </Stack>
            </Stack>
            <Divider sx={{ mb: 2 }} />
            
            {/* Affichage des états (Chargement/Vide) */}
            {loading && (
              <Box display="flex" justifyContent="center" py={3}>
                <CircularProgress size={28} />
              </Box>
            )}
            {!loading && sessions.length === 0 && (
              <Typography color="text.secondary">Aucune session trouvée.</Typography>
            )}

            {/* Liste des sessions */}
            <Stack spacing={2}>
              {sessions.map(s => (
                <Card key={s.id_session} variant="outlined" sx={componentStyles.sessionCard}>
                  <CardContent>
                    <Stack direction="row" justifyContent="space-between" alignItems="flex-start">
                      <Box>
                        <Typography variant="subtitle1" fontWeight={600}>
                          {s.titre}
                        </Typography>
                        <Typography variant="caption" color="text.secondary">
                          Code: {s.id_session} - Mode de jeu: {s.mode_de_jeu}
                        </Typography>
                        </Box>
                      {/* Utilisation de la fonction d'aide pour le statut */}
                      {getStatusChip(s.status)} 
                    </Stack>

                    {/* Affichage des stories */}
                    <Stack spacing={1} mt={2}>
                      {s.stories && s.stories.map((story, index) => (
                        <Box key={story.titre + index} sx={componentStyles.storyBox}>
                          <Typography variant="subtitle2" fontWeight={500}>
                            {story.titre}
                          </Typography>
                          <Typography variant="body2" color="text.secondary">
                            {story.contenu}
                          </Typography>
                          <Typography variant="caption" color="text.secondary">
                            Valeur: {story.valeur_finale}
                          </Typography>
                        </Box>
                      ))}
                    </Stack>
                  </CardContent>
                </Card>
              ))}
            </Stack>

          </CardContent>
        </Card>
      </Stack>
    </Container>
  );
}