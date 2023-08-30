from django.urls import path
from .views import *

urlpatterns = [
    #path('t',TodoView.as_view(), name='todo'),
    path('client-list/',              ClientListView.as_view(),name='client-list'),
    path('client',              ClientCreateView.as_view(),name='client'),
    path('client/<int:pk>/update',ClientUpdateView.as_view(),name='client-edit'),
    path('client/<int:pk>/delete',ClientDeleteView.as_view(),name='client-del'),
    path('client/<int:pk>/detail',ClientDetaiView.as_view(),name='client-detai'),
    
    path('agence-list/',          AgenceListView.as_view(),name='agence-list'),
    path('agence/',               AgenceCreateView.as_view(),name='agence'),
    path('agence/<int:pk>/update',AgenceUpdateView.as_view(),name='agence_up'),
    path('agence/<int:pk>/delete',AgenceDeleteView.as_view(),name='agence_del'),
    path('agence/<int:pk>/detail',AgenceDetaiView.as_view(),name='agence-detai'),
    
]
