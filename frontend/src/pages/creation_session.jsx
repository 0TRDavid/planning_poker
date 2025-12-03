import React, { useState, useRef } from 'react';
import { Container, Typography, Stack, Button, Card, CardContent, Divider, FormControl, RadioGroup, FormControlLabel, Radio, Alert} from '@mui/material';
import UploadFileIcon from '@mui/icons-material/UploadFile';
import SendIcon from '@mui/icons-material/Send';
import { createSession } from '../services/api';

// --- STYLES ---
const componentStyles = {
    card: {
        borderRadius: 3,
        maxWidth: 600,
        margin: '0 auto',
        padding: 2,
    },
    title: {
        fontWeight: 600,
        mb: 1,
    },
    sectionTitle: {
        fontWeight: 500,
        mt: 2,
        mb: 1,
        color: 'primary.main',
    },
    radioGroup: {
        flexDirection: 'row', // Affichage des options en ligne
        justifyContent: 'space-between',
        flexWrap: 'wrap',
    },
    fileInput: {
        display: 'none',
    },
};

export default function ModeSelection() {
    const [gameMode, setGameMode] = useState('strict');
    const [fileData, setFileData] = useState(null);
    const [error, setError] = useState('');
    const fileInputRef = useRef(null);

    const modes = [
        { value: 'strict', label: 'Stricte (Unanimité)' },
        { value: 'median', label: 'Médiane' },
        { value: 'average', label: 'Moyenne' },
        { value: 'majority_abs', label: 'Majorité Absolue' },
        { value: 'majority_rel', label: 'Majorité Relative' },
    ];

    const handleFileChange = (event) => {
        const file = event.target.files[0];
        if (!file) return;

        if (file.type !== 'application/json') {
            setError("Veuillez importer un fichier au format JSON.");
            setFileData(null);
            return;
        }

        const reader = new FileReader();
        reader.onload = (e) => {
            try {
                const jsonContent = JSON.parse(e.target.result);
                console.log("Fichier JSON chargé:", jsonContent);
                setFileData(jsonContent);
                setError('');
            } catch (err) {
                setError("Erreur lors de la lecture du fichier JSON. Assurez-vous qu'il est valide.");
                setFileData(null);
            }
        };
        reader.readAsText(file);
    };

const handleSaveAndRedirect = async () => { 
    if (!fileData || fileData.length === 0) {
        setError("Veuillez importer au moins une User Story.");
        return;
    }

    try {
        const titreSession = "Nouvelle Session - " + new Date().toLocaleString();
        const newSession = await createSession(titreSession, fileData); 
        //window.location.href = `/partie/${newSession.id_session}?mode=${gameMode}`; 
        window.location.href = `/accueiluser`;

    } catch (e) {
        setError(`Échec de la création de session : ${e.message}`);
    }
};
    return (
        <Container maxWidth="md" sx={{ py: 6, paddingTop: '100px' }}>
            <Card variant="outlined" sx={componentStyles.card}>
                <CardContent>
                    <Typography variant="h5" component="h1" sx={componentStyles.title}>
                        Création de Session
                    </Typography>
                    <Typography variant="body2" color="text.secondary" mb={3}>
                        Sélectionnez le mode de jeu et importez vos User Stories.
                    </Typography>

                    {/* 1. Sélection du Mode de Jeu */}
                    <Divider />
                    <Typography variant="subtitle1" sx={componentStyles.sectionTitle}>
                        Mode de Jeu
                    </Typography>
                    <FormControl component="fieldset" fullWidth>
                        <RadioGroup
                            name="game-mode"
                            value={gameMode}
                            onChange={(e) => setGameMode(e.target.value)}
                            sx={componentStyles.radioGroup}
                        >
                            {modes.map((mode) => (
                                <FormControlLabel
                                    key={mode.value}
                                    value={mode.value}
                                    control={<Radio size="small" />}
                                    label={mode.label}
                                />
                            ))}
                        </RadioGroup>
                    </FormControl>

                    <Divider sx={{ mt: 3, mb: 3 }} />

                    {/* 2. Importation des Données JSON */}
                    <Typography variant="subtitle1" sx={componentStyles.sectionTitle}>
                        Importation des User Stories
                    </Typography>
                    
                    {error && <Alert severity="error" sx={{ mb: 2 }}>{error}</Alert>}
                    
                    <Stack spacing={2} direction={{ xs: 'column', sm: 'row' }}>
                        {/* Champ de fichier masqué */}
                        <input
                            type="file"
                            accept=".json"
                            ref={fileInputRef}
                            onChange={handleFileChange}
                            style={componentStyles.fileInput}
                        />
                        
                        {/* Bouton d'importation */}
                        <Button
                            variant="outlined"
                            startIcon={<UploadFileIcon />}
                            onClick={() => fileInputRef.current.click()}
                            sx={{ flex: 1 }}
                        >
                            Importer JSON
                        </Button>
                        
                        {/* Bouton d'enregistrement et de redirection */}
                        <Button
                            variant="contained"
                            startIcon={<SendIcon />}
                            onClick={handleSaveAndRedirect}
                            disabled={!fileData}
                            sx={{ flex: 1 }}
                        >
                            Enregistrer & Continuer
                        </Button>
                    </Stack>
                    
                    {fileData && (
                        <Alert severity="info" sx={{ mt: 2 }}>
                            Fichier chargé. Prêt à enregistrer {fileData.user_stories ? fileData.user_stories.length : 'les'} stories.
                        </Alert>
                    )}
                </CardContent>
            </Card>
        </Container>
    );
}