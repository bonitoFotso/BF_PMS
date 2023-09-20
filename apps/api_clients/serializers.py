from rest_framework import serializers
from apps.clients.models import Client, Agence, Appelant

class ClientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Client
        fields = '__all__'  # Incluez tous les champs du modèle dans la sérialisation


class AgenceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Agence
        fields = '__all__'

class AppelantSerializer(serializers.ModelSerializer):
    class Meta:
        model = Appelant
        fields = '__all__'
  