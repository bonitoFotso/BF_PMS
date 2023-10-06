from rest_framework import serializers
from apps.project.models import Tache,Categorie, Activite
from apps.clients.models import  Appelant

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
