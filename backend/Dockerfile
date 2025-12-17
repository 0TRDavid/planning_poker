FROM python:3.12
# Définir le répertoire de travail
WORKDIR /app

# Installer les dépendances système nécessaires pour python-ldap
RUN apt-get update && apt-get install -y \
    build-essential \
    libldap2-dev \
    libsasl2-dev \
    libssl-dev \
    && rm -rf /var/lib/apt/lists/*
    
# Copier requirements et installer dépendances Python
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copier tout le projet
COPY . .

# Collecte des fichiers statiques
RUN python manage.py collectstatic --noinput

# Exposer le port HTTPS
EXPOSE 8001
CMD ["gunicorn", "-b", "0.0.0.0:8000", "backend.wsgi:application"]
