from rest_framework import generics
from apps.project.models import Tache,Categorie, Activite
from apps.clients.models import  Appelant
from .serializers import TacheSerializer,CategorieSerializer, ActiviteSerializer, AppelantSerializer


class TacheListCreateView(generics.ListCreateAPIView):
    queryset = Tache.objects.all()
    serializer_class = TacheSerializer
    
#class TechnicienTacheListCreateView(generics.ListCreateAPIView):
#    queryset = TechnicienTache.objects.all()
#    serializer_class = TechnicienTacheSerializer
#    
#class RapportListCreateView(generics.ListCreateAPIView):
#    queryset = Rapport.objects.all()
#    serializer_class = RapportSerializer
    

class CategorieListCreateView(generics.ListCreateAPIView):
    queryset = Categorie.objects.all()
    serializer_class = CategorieSerializer

class CategorieDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Categorie.objects.all()
    serializer_class = CategorieSerializer

class ActiviteListCreateView(generics.ListCreateAPIView):
    queryset = Activite.objects.all()
    serializer_class = ActiviteSerializer

class ActiviteDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Activite.objects.all()
    serializer_class = ActiviteSerializer

class AppelantListCreateView(generics.ListCreateAPIView):
    queryset = Appelant.objects.all()
    serializer_class = AppelantSerializer

class AppelantDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Appelant.objects.all()
    serializer_class = AppelantSerializer
