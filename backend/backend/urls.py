from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from planning_poker import views

router = DefaultRouter()
router.register(r'sessions', views.SessionViewSet, basename='session')
router.register(r'parties', views.PartieViewSet, basename='partie')

urlpatterns = [
    path("admin/", admin.site.urls),
    path('api/', include(router.urls)),  # Utilisation de la vue join_partie
]
