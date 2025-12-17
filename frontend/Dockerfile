# Image de base Node.js
FROM node:22

# Définir le répertoire de travail
WORKDIR /app

# Copier package.json et package-lock.json pour profiter du cache Docker
COPY package.json package-lock.json ./

# Installer les dépendances
RUN npm install

# Copier le reste du code source
COPY . .

# Construire l'application pour la production
RUN npm run build

# Exposer le port 5171
EXPOSE 5173

# Lancer le serveur Vite Preview sur le port 5171
CMD ["npx", "vite", "preview", "--port", "5173", "--host"]
