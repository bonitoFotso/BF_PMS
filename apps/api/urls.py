from django.urls import path
from .views import TacheListCreateView, CategorieListCreateView, CategorieDetailView, ActiviteListCreateView, ActiviteDetailView, AppelantListCreateView, AppelantDetailView

urlpatterns = [
    path('taches/', TacheListCreateView.as_view(), name='tache-list-create'),
    
    path('categories/', CategorieListCreateView.as_view(), name='categorie-list-create'),
    path('categories/<int:pk>/', CategorieDetailView.as_view(), name='categorie-detail'),

    path('activites/', ActiviteListCreateView.as_view(), name='activite-list-create'),
    path('activites/<int:pk>/', ActiviteDetailView.as_view(), name='activite-detail'),

    path('appelants/', AppelantListCreateView.as_view(), name='appelant-list-create'),
    path('appelants/<int:pk>/', AppelantDetailView.as_view(), name='appelant-detail'),
    
    # Ajoutez des URL similaires pour les modèles Agence et Appelant si nécessaire
]