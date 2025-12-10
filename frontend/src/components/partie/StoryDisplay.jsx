// src/components/partie/StoryDisplay.jsx
import React from 'react';
import { Card, CardContent, Typography, Stack, Button } from '@mui/material';
import VisibilityIcon from '@mui/icons-material/Visibility';
import VisibilityOffIcon from '@mui/icons-material/VisibilityOff';
import SkipNextIcon from '@mui/icons-material/SkipNext';

// AJOUT DE LA PROP 'onNext'
export default function StoryDisplay({ currentStory, showVotes, onReveal, onNext }) {
    return (
        <Card variant="outlined" sx={{ minHeight: '200px', p: 3, textAlign: 'center', background: '#f8f8ff' }}>
            <CardContent>
                <Typography variant="h6" color="text.primary" gutterBottom>
                    {currentStory?.titre || "Chargement..."}
                </Typography>
                <Typography variant="body1" color="text.secondary">
                    {currentStory?.contenu}
                </Typography>
                
                <Stack direction="row" spacing={2} justifyContent="center" mt={3}>
                    <Button 
                        variant="contained" 
                        color={showVotes ? "error" : "primary"}
                        onClick={onReveal}
                        startIcon={showVotes ? <VisibilityOffIcon /> : <VisibilityIcon />}
                        disabled={showVotes || !currentStory}
                    >
                        {showVotes ? "Votes Révélés" : "Révéler les votes"}
                    </Button>
                    
                    {/* Le bouton Next apparaît uniquement quand les votes sont révélés */}
                    {showVotes && (
                        <Button 
                            variant="outlined" 
                            startIcon={<SkipNextIcon />}
                            onClick={onNext} // <--- Connexion ici
                        >
                            Story Suivante
                        </Button>
                    )}
                </Stack>
            </CardContent>
        </Card>
    );
}