from django.db import models
from django.utils.translation import gettext_lazy as _
from django.conf import settings
from apps.authentication.models import User 
# Create your models here.

class Technicien(models.Model):
    user = models.OneToOneField(User, verbose_name=_("User"), on_delete=models.CASCADE,null=True)
    photo = models.ImageField(_("profile"), upload_to='media/profile', )
    nom  = models.CharField(_("nom"), max_length=50)
    prenom = models.CharField(_("prenom"), max_length=50)
    tel = models.CharField(_("telephone"),max_length=20)
    email = models.EmailField(max_length=254)
    matricule = models.CharField(_("matricune"), unique=True,max_length=20)
    date_add = models.DateTimeField(auto_now_add=True) 
    date_upd = models.DateTimeField(auto_now=True)
    vitesse_execution = models.FloatField(_("Vitesse d'exécution"), default=0.0)
    efficacite = models.FloatField(_("Efficacité"), default=0.0)
    
    def __str__(self):
        return self.nom
    
    
    class Meta:
        
        managed = True
        verbose_name = 'Technicien'
        verbose_name_plural = 'Techniciens'
        
class StateDay(models.Model):
    technicien = models.ForeignKey("Technicien", verbose_name=_("echnicien"), on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now=True, auto_now_add=False)
    
    

    def __str__(self):
        return 
