from rest_framework import generics
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from apps.clients.models import Client, Agence, Appelant
from .serializers import ClientSerializer, AgenceSerializer, AppelantSerializer

# Importez vos sérialiseurs pour Client, Agence et Appelant

class ClientListCreateView(generics.ListCreateAPIView):
    queryset = Client.objects.all()
    serializer_class = ClientSerializer

class ClientRetrieveUpdateDeleteView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Client.objects.all()
    serializer_class = ClientSerializer

class AgenceListAPIView(generics.ListCreateAPIView):
    queryset = Agence.objects.all()
    serializer_class = AgenceSerializer

class AgenceDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Agence.objects.all()
    serializer_class = AgenceSerializer

class AppelantListAPIView(generics.ListCreateAPIView):
    queryset = Appelant.objects.all()
    serializer_class = AppelantSerializer

class AppelantDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Appelant.objects.all()
    serializer_class = AppelantSerializer

class ClientListJson(APIView):
    def get(self, request):
        clients = Client.objects.all()
        serializer = ClientSerializer(clients, many=True)
        return Response(serializer.data)

# Définissez des vues similaires pour Agence et Appelant si nécessaire

class AgenceListCreateView(generics.ListCreateAPIView):
    queryset = Agence.objects.all()
    serializer_class = AgenceSerializer

class AgenceRetrieveUpdateDeleteView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Agence.objects.all()
    serializer_class = AgenceSerializer

class AppelantListCreateView(generics.ListCreateAPIView):
    queryset = Appelant.objects.all()
    serializer_class = AppelantSerializer

class AppelantRetrieveUpdateDeleteView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Appelant.objects.all()
    serializer_class = AppelantSerializer
    
@method_decorator(csrf_exempt, name='dispatch')
class M(APIView):
    def post(self, request):
        # Traitement des données POST
        return Response({"message": "Demande POST réussie"}, status=status.HTTP_201_CREATED)

    def get(self, request):
        # Traitement des demandes GET
        return Response({"message": "Demande GET réussie"})

    # Autres méthodes HTTP et logique de vue