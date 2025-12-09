from django.urls import path, include
urlpatterns = [
    path('', include('router.urls')),  # Nécessaire si urls séparées
]