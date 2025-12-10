import React from 'react';
import { Box, Typography, Paper, Tooltip, Stack } from '@mui/material';
import { getCardSvg } from '../../services/card';

// Styles simplifiés et stricts
const styles = {
    scrollContainer: {
        overflowX: 'auto',      // Active le scroll horizontal
        padding: 1,
        paddingBottom: 2,       // Espace pour la barre de défilement
        width: '100%',          // Prend toute la largeur disponible
    },
    card: {
        width: '130px',          // 1. LARGEUR FIXE : C'est la clé pour forcer la taille
        height: '200px',        // 2. HAUTEUR FIXE (ratio 2/3 de 70px)
        flexShrink: 0,          // 3. Empêche l'écrasement dans la Stack
        transition: 'all 0.2s ease',
        borderRadius: 3,
        '&:hover': {
            transform: 'translateY(-2px)',
            boxShadow: 3,
        },
    },
    selected: {
        border: '2px solid',
        borderColor: 'primary.main',
        transform: 'scale(1.05)',
        boxShadow: 4,
    },
    svgContainer: {
        width: '100%',
        height: '100%',
        display: 'flex',        // Centre le SVG parfaitement
        justifyContent: 'center',
        alignItems: 'center',
        '& > svg': {            // Cible directement le SVG injecté
            width: '100%',
            height: '100%',
            objectFit: 'contain' // Garde les proportions sans déborder
        }
    }
};

export default function VotingDeck({ cardSet, selectedCard, onVote }) {
    return (
        <Box>
            <Typography variant="h6" fontWeight={600} mb={2}>
                Sélectionnez votre estimation :
            </Typography>
            
            <Box sx={styles.scrollContainer}>
                {/* Stack remplace Grid pour une ligne simple : plus léger, plus facile à contrôler */}
                <Stack direction="row" spacing={1} justifyContent={{ mx: 'auto', width: 'fit-content'}}>
                    {cardSet.map(value => (
                        <Paper
                            key={value}
                            elevation={selectedCard === value ? 8 : 2}
                            onClick={() => onVote(value)}
                            sx={{
                                ...styles.card,
                                ...(selectedCard === value && styles.selected)
                            }}
                        >
                            <Tooltip title={`Voter ${value}`}>
                                <Box sx={styles.svgContainer}>
                                    {getCardSvg(value)}
                                </Box>
                            </Tooltip>
                        </Paper>
                    ))}
                </Stack>
            </Box>
        </Box>
    );
}