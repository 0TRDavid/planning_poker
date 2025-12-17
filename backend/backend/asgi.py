"""!
@brief Point d'entrée ASGI pour les serveurs web asynchrones (Uvicorn, Daphne).

Permet de gérer des connexions asynchrones (WebSockets) si nécessaire dans le futur.
Expose l'application callable `application`.
"""

import os

from django.core.asgi import get_asgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')

application = get_asgi_application()