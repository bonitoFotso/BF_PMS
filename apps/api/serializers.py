from rest_framework import serializers
from apps.project.models import Tache,Categorie, Activite
from apps.clients.models import  Appelant,Client,Agence

class TacheSerializer(serializers.ModelSerializer):
    activite_nom = serializers.CharField(source='activite.nom')
    categorie_nom = serializers.CharField(source='categorie.nom')
    appelant_nom = serializers.CharField(source='appelant.name')

    class Meta:
        model = Tache
        fields = '__all__'
        

class CategorieSerializer(serializers.ModelSerializer):
    class Meta:
        model = Categorie
        fields = '__all__'

class ActiviteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Activite
        fields = '__all__'

class AppelantSerializer(serializers.ModelSerializer):
    class Meta:
        model = Appelant
        fields = '__all__'

class ClientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Client
        fields = '__all__'  # Incluez tous les champs du modèle dans la sérialisation


class AgenceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Agence
        fields = '__all__'