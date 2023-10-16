from django.urls import path
from .views import (TacheListCreateView, TacheDetailView, CategorieListCreateView, CategorieDetailView, ActiviteListCreateView, ActiviteDetailView, AppelantListCreateView, AppelantDetailView,
ClientListCreateView, ClientDetailView, AgenceListCreateView, AgenceDetailView,TechnicienListCreateView,TechnicienDetailView
)
from .auth_views import *

urlpatterns = [
    path('taches/', TacheListCreateView.as_view(), name='tache-list-create'),
    path('taches/<int:pk>', TacheDetailView.as_view(), name='taches-detail'),

    path('categories/', CategorieListCreateView.as_view(), name='categorie-list-create'),
    path('categories/<int:pk>/', CategorieDetailView.as_view(), name='categorie-detail'),

    path('activites/', ActiviteListCreateView.as_view(), name='activite-list-create'),
    path('activites/<int:pk>/', ActiviteDetailView.as_view(), name='activite-detail'),

    path('appelants/', AppelantListCreateView.as_view(), name='appelant-list-create'),
    path('appelants/<int:pk>/', AppelantDetailView.as_view(), name='appelant-detail'),
    
    # URL pour les vues de la client
    path('clients/',ClientListCreateView.as_view(), name='client-list-create'),
    path('clients/<int:pk>/', ClientDetailView.as_view(), name='client-detail'),

    # URL pour les vues de l'agence
    path('agences/', AgenceListCreateView.as_view(), name='agence-list-create'),
    path('agences/<int:pk>/', AgenceDetailView.as_view(), name='agence-detail'),
    
    path('techniciens/', TechnicienListCreateView.as_view(), name='technicien-list-create'),
    path('techniciens/<int:pk>/', TechnicienDetailView.as_view(), name='technicien-detail'),
    #
    #path('login/', LoginApi.as_view()),
    #path('register/', RegisterApi.as_view()),
    # Ajoutez des URL similaires pour les modèles Agence et Appelant si nécessaire
]