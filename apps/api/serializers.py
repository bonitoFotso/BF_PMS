from rest_framework import serializers
from apps.project.models import Tache,Categorie, Activite
from apps.clients.models import  Appelant,Client,Agence
from apps.ressource.models import Technicien
from apps.authentication.models import User


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
        


class TechnicienSerializer(serializers.ModelSerializer):
    class Meta:
        model = Technicien
        fields = '__all__'



class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'email', 'password')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User.objects.create_user(
            #username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password']
        )
        return user
