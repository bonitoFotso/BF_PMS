from django.db import models
from django.utils.translation import gettext_lazy as _
from django.conf import settings
# Create your models here.

class Technicien(models.Model):
    photo = models.ImageField(_("profile"), upload_to='profile', )
    nom  = models.CharField(_("nom"), max_length=50)
    prenom = models.CharField(_("prenom"), max_length=50)
    tel = models.CharField(_("telephone"),max_length=20)
    email = models.EmailField(max_length=254)
    matricule = models.CharField(_("matricune"), unique=True,max_length=20)
    date_add = models.DateTimeField(auto_now_add=True) 
    date_upd = models.DateTimeField(auto_now=True) 
    
    def __str__(self):
        return self.nom
    
    class Meta:
        db_table = ''
        managed = True
        verbose_name = 'Technicien'
        verbose_name_plural = 'Techniciens'