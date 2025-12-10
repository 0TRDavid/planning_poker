from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from planning_poker import views

router = DefaultRouter()
router.register(r'sessions', views.SessionViewSet)
router.register(r'joinPartie', views.JoinPartieViewSet, basename='joinPartie')
router.register(r'parties', views.PartieViewSet, basename='partie')


# Dans urls.py, affiche tous les basenames enregistrés
print("Basenames enregistrés:")
for prefix, viewset, basename in router.registry:
    print(f"  - {prefix:20} → {basename}")

urlpatterns = [
    path("admin/", admin.site.urls),
    path('api/', include(router.urls)),
]
