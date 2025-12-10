import React from 'react';
import { Container, TextField, Button, Typography, Box, Paper } from '@mui/material';

const Accueil = () => {
    const [username, setUsername] = React.useState('');
    const [error, setError] = React.useState('');

    React.useEffect(() => {
        // Logique pour récupérer le nom d'utilisateur depuis les cookies
        const match = document.cookie.match(/(?:^|;\s*)username=([^;]+)/);
        if (match) setUsername(decodeURIComponent(match[1]));
    }, []);

    const handleSubmit = (e) => {
        e.preventDefault();
        const value = username.trim();
        
        if (!value) {
            setError("Le nom d'utilisateur est requis");
            return;
        }

        // Définir le cookie
        const expires = new Date(Date.now() + 30*24*60*60*1000).toUTCString();
        document.cookie = `username=${encodeURIComponent(value)}; expires=${expires}; path=/; SameSite=Lax`;
        
        // Redirection
        window.location.href = '/accueiluser';
    };

    return (
        <Container maxWidth="sm" sx={{ paddingTop: '85px', minHeight: '80vh', display: 'flex', alignItems: 'center', justifyContent: 'center' }}>
            <Paper elevation={8} sx={{padding: 3, textAlign: 'center', height: 'fit-content', width: '70%'}}>
                <Typography variant="h4" component="h1" sx={{ marginBottom: 0 }}>
                    Planning Poker
                </Typography>
                <Typography variant="body2" >
                    Entrez votre nom d'utilisateur pour continuer.
                </Typography>
                <Box component="form" onSubmit={handleSubmit} noValidate >
                    <TextField
                        label="Nom d'utilisateur"
                        value={username}
                        onChange={(e) => {
                            setUsername(e.target.value);
                            if (error) setError('');
                        }}
                        fullWidth
                        autoFocus
                        required
                        margin="normal"
                        error={Boolean(error)}
                        helperText={error || ' '}
                    />
                    <Button 
                        type="submit" 
                        variant="contained" 
                        fullWidth 
                        size="large"
                        className="accueil-button"
                    >
                        Entrer
                    </Button>
                </Box>
            </Paper>
        </Container>
    );
};

export default Accueil;