from django.urls import path, re_path
from .views import *

urlpatterns = [
    path("technicien-create", TechnicienCreateView.as_view(), name="technicien-create"),
    path("technicien-list", TechnicienListView.as_view(), name="technicien-list"),
    path('technicien/<int:pk>/detail',TechnicienDetailView.as_view(),name='technicien-detail'),
    path('accounts/', AccountView.as_view(), name='account'),
    
    path('compute/', compute, name="compute"),
    path('c', Comp.as_view(), name='c'),
    
    path('api/technicien/', TechnicienListJson.as_view(), name='technicien-list-json'),

    
    
]


