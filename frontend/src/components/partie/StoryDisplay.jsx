import React from 'react';
import { Card, CardContent, Typography, Stack, Button } from '@mui/material';
import VisibilityIcon from '@mui/icons-material/Visibility';
import VisibilityOffIcon from '@mui/icons-material/VisibilityOff';
import RefreshIcon from '@mui/icons-material/Refresh';

export default function StoryDisplay({ currentStory, showVotes, onReveal }) {
    return (
        <Card variant="outlined" sx={{ minHeight: '100px', p: 3, textAlign: 'center', background: '#f8f8ff' }}>
            <CardContent>
                <Typography variant="h6" color="text.secondary" gutterBottom>{currentStory?.titre || "En attente de story..."}</Typography>
                <Typography variant="body1" color="text.secondary">{currentStory?.contenu}</Typography>
                                
                <Stack direction="row" justifyContent="center" mt={3} spacing={2}>
                    <Button 
                        variant="contained" 
                        color={showVotes ? "error" : "primary"}
                        onClick={onReveal}
                        startIcon={showVotes ? <VisibilityOffIcon /> : <VisibilityIcon />}
                        disabled={showVotes || !currentStory}
                    >
                        {showVotes ? "Votes Révélés" : "Révéler les votes"}
                    </Button>
                    
                    {showVotes && (
                        <Button variant="outlined" startIcon={<RefreshIcon />}> Story Suivante </Button>
                    )}
                </Stack>
            </CardContent>
        </Card>
    );
}