import React, { useState, useEffect } from 'react';
import PlayArrowIcon from '@mui/icons-material/PlayArrow';
import AddIcon from '@mui/icons-material/Add';
import RefreshIcon from '@mui/icons-material/Refresh';

import {
  Box,
  Container,
  Typography,
  Stack,
  Button,
  TextField,
  Card,
  CardContent,
  CardActions,
  Chip,
  Divider,
  CircularProgress
} from '@mui/material';



//API qui va appeler les sessions existantes dans le back
const fetchSessions = async () => {
  const response = await fetch('http://localhost:8000/api/sessions/'); // URL de votre API Django
  const sessions = await response.json();
  console.log(sessions);
  return sessions;
};

export default function AccueilUser() {
  const [sessions, setSessions] = useState([]);
  const [loading, setLoading] = useState(false);
  const [joinCode, setJoinCode] = useState('');
  const [creating, setCreating] = useState(false);

  const loadSessions = async () => {
    setLoading(true);
    try {
      const data = await fetchSessions();  // On appel la fonction de récupération des sessions
      setSessions(data);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadSessions();
  }, []);

  const handleJoin = () => {
    if (!joinCode.trim()) return;
    // Logique de connexion à la session (à intégrer avec le backend)
    alert('Join session: ' + joinCode);
    setJoinCode('');
  };

  const handleCreate = async () => {
    setCreating(true);
    // Logique de création de session (à intégrer avec le backend)
    await new Promise(r => setTimeout(r, 500));
    alert('Session créée');
    setCreating(false);
    loadSessions();
  };

  return (
    
    <Container maxWidth="md" sx={{ py: 6 }}>
      <Stack spacing={4}>
        <Box>
          <Typography variant="h4" fontWeight={600}>
            Planning Poker
          </Typography>
          <Typography variant="body1" color="text.secondary">
            Gérez vos sessions et rejoignez une estimation.
          </Typography>
        </Box>

        {/* Carte pour rejoindre une session */}
        <Card variant="outlined">
          <CardContent>
            <Stack spacing={2}>
              <Typography variant="h6">Rejoindre une session</Typography>
              <Stack direction={{ xs: 'column', sm: 'row' }} spacing={2}>
                <TextField
                  label="Code session"
                  value={joinCode}
                  onChange={e => setJoinCode(e.target.value.toUpperCase())}
                  inputProps={{ maxLength: 10, style: { letterSpacing: 2 } }}
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

        {/* Carte affichant les sessions de l'utilisateur */}
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
            {loading && (
              <Box display="flex" justifyContent="center" py={3}>
                <CircularProgress size={28} />
              </Box>
            )}
            {!loading && sessions.length === 0 && (
              <Typography color="text.secondary">Aucune session.</Typography>
            )}
            <Stack spacing={2}>
              {sessions.map(s => (
                <Card key={s.id_session} variant="outlined" sx={{ borderRadius: 2 }}>
                  <CardContent>
                    <Stack direction="row" justifyContent="space-between" alignItems="flex-start">
                      <Box>
                        <Typography variant="subtitle1" fontWeight={600}>
                          {s.titre}
                        </Typography>
                        <Typography variant="caption" color="text.secondary">
                          Code: {s.id_session}
                        </Typography>
                      </Box>
                      <Chip
                        size="small"
                        label={
                          s.status === 'open'
                            ? 'Ouverte'
                            : s.status === 'in-progress'
                            ? 'En cours'
                            : 'Terminée'
                        }
                        color={
                          s.status === 'open'
                            ? 'success'
                            : s.status === 'in-progress'
                            ? 'warning'
                            : 'default'
                        }
                      />
                    </Stack>

                    {/* Affichage de la liste des stories */}
                    <Stack spacing={1} mt={2}>
                      {s.stories.map((story, index) => (
                        <Box key={story.titre + index} sx={{ border: '1px solid #ccc', p: 1, borderRadius: 1 }}>
                          <Typography variant="subtitle2" fontWeight={500}>
                            {story.titre}
                          </Typography>
                          <Typography variant="body2" color="text.secondary">
                            {story.contenu}
                          </Typography>
                          <Typography variant="caption" color="text.secondary">
                            Valeur: {story.valeur}
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
