from django.urls import path
from . import views

urlpatterns = [
    path('clients/', views.ClientListCreateView.as_view(), name='client-list-create'),
    path('clients/<int:pk>/', views.ClientRetrieveUpdateDeleteView.as_view(), name='client-retrieve-update-delete'),
    path('agences/', views.AgenceListCreateView.as_view(), name='agence-list-create'),
    path('agences/<int:pk>/', views.AgenceRetrieveUpdateDeleteView.as_view(), name='agence-retrieve-update-delete'),
    path('appelants/', views.AppelantListCreateView.as_view(), name='appelant-list-create'),
    path('appelants/<int:pk>/', views.AppelantRetrieveUpdateDeleteView.as_view(), name='appelant-retrieve-update-delete'),
    path('cl/',views.ClientListJson.as_view(),name='cl'),
    path('m/',views.M.as_view(),name='m'),
    # Ajoutez des URL similaires pour les modèles Agence et Appelant si nécessaire
]
