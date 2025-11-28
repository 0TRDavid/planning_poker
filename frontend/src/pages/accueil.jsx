import React from 'react';
import '../assets/accueil.css';
import { Container, TextField, Button, Typography, Box, Paper } from '@mui/material';

const Accueil = () => {
    const [username, setUsername] = React.useState('');
    const [error, setError] = React.useState('');

    React.useEffect(() => {
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
        const expires = new Date(Date.now() + 30*24*60*60*1000).toUTCString();
        document.cookie = `username=${encodeURIComponent(value)}; expires=${expires}; path=/; SameSite=Lax`;
        window.location.href = '/accueiluser';
    };

    return (
        <Container maxWidth="sm" className="accueil-container">
            <div className="accueil-center">
                <Paper elevation={4} className="accueil-card">
                    <Typography variant="h4" component="h1" className="accueil-title">
                        Planning Poker
                    </Typography>
                    <Typography variant="body2" className="accueil-subtitle">
                        Entrez votre nom d'utilisateur pour continuer.
                    </Typography>
                    <Box component="form" onSubmit={handleSubmit} noValidate className="accueil-form">
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
                        <Button type="submit" variant="contained" fullWidth className="accueil-button">
                            Entrer
                        </Button>
                    </Box>
                </Paper>
            </div>
        </Container>
    );
};

export default Accueil;
