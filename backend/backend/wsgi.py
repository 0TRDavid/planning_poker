"""!
@brief Point d'entrée WSGI pour les serveurs web compatibles (Gunicorn, Apache).

Expose l'application Django callable nommée `application` pour le déploiement en production
dans un environnement synchrone standard.
"""

import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')

application = get_wsgi_application()