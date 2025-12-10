import React from 'react';
import { Box, Typography, Grid, Paper, Chip } from '@mui/material';
import CheckCircleOutlineIcon from '@mui/icons-material/CheckCircleOutline';

export default function PlayersGrid({ votes, username, hasVoted, showVotes }) {
    // Calcul du nombre de joueurs (autres + moi)
    const playerCount = Object.keys(votes).length + 1;

    return (
        <Box>
            <Typography variant="subtitle1" fontWeight={600} mb={1}>
                Joueurs ({playerCount} en ligne)
            </Typography>
            <Grid container spacing={2}>
                {/* 1. Carte de l'utilisateur actuel (Moi) */}
                <Grid item xs={6} sm={3}>
                    <Paper elevation={3} sx={{ p: 1.5, textAlign: 'center' }}>
                        <Typography variant="subtitle2" sx={{ fontWeight: 700 }}>Moi ({username})</Typography>
                        {hasVoted ? (
                            <Chip label="Voté" color="success" size="small" icon={<CheckCircleOutlineIcon />} sx={{ mt: 1 }} />
                        ) : (
                            <Chip label="En attente" color="default" size="small" sx={{ mt: 1 }} />
                        )}
                    </Paper>
                </Grid>

                {/* 2. Cartes des autres joueurs */}
                {Object.entries(votes).map(([player, voteValue]) => (
                    <Grid item xs={6} sm={3} key={player}>
                        <Paper elevation={2} sx={{ p: 1.5, textAlign: 'center' }}>
                            <Typography variant="subtitle2">{player}</Typography>
                            {showVotes ? (
                                <Typography variant="h5" sx={{ mt: 1 }}>
                                    {voteValue !== null ? voteValue : '🤷'}
                                </Typography>
                            ) : (
                                <Chip 
                                    label={voteValue ? "Voté" : "En attente"} 
                                    color={voteValue ? "primary" : "default"} 
                                    size="small" 
                                    sx={{ mt: 1 }} 
                                />
                            )}
                        </Paper>
                    </Grid>
                ))}
            </Grid>
        </Box>
    );
}