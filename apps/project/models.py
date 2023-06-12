from django.db import models
#from apps.authentication.models import User    
from django.utils.translation import gettext_lazy as _
from django.core.validators import MaxValueValidator, MinValueValidator 
from django.db.models.signals import post_save
from django.dispatch import receiver
from apps.clients.models import *
from apps.ressource.models import *
# Create your models here.
prio = [
    ('Bas','Bas'),
    ('Moyen','Moyen'),
    ('Elever','Elever'),
]

status = [
		('En atente', 'En atente'),
		('En cours', 'En cours'),
		('En arret', 'En arret'),
		('En facturation', 'En facturation')
		]

class Etat(models.Model):
    nom = models.CharField(_("nom de l'etat"), choices=status,max_length=20)
    description = models.CharField(_("des criprion de l'etat"), max_length=50)
    motif = models.CharField(_("motif de l'etat"), max_length=50,default='RAS')

    def __str__(self):
        return '{0}:{1}'.format(self.nom,self.motif)

class Tache(models.Model):
    nom = models.CharField(_("name"), max_length=50)
    appelant = models.ForeignKey(Appelant, verbose_name=_(" celui qui appel "), on_delete=models.CASCADE)
    agence = models.ForeignKey(Agence,on_delete=models.CASCADE,max_length=20 )
    priorite = models.CharField(choices=prio, max_length=20, )
    description = models.CharField(max_length=500,null=False, default='description')
    n_OS = models.CharField(_("numero d OS"), max_length=50,null=True,blank=True)
    etat = models.ForeignKey("Etat", verbose_name=_("etat"), on_delete=models.CASCADE)
    ok = models.BooleanField(default=False)
    observation = models.CharField(max_length=100, default='observation')
    date_debut = models.DateField(_("date de debut"),blank=True,null=True)
    date_fin = models.DateField(_("date de fin"),blank=True,null=True)
    technicien = models.ForeignKey(Technicien, verbose_name=_("Tecnicien"), on_delete=models.CASCADE)
    createdAt = models.DateTimeField(auto_now_add=True)
    updatedAt = models.DateTimeField(auto_now=True)
    #tec = models.ForeignKey("TechnicienTache", verbose_name=_(""), on_delete=models.CASCADE)
    
    def __str__(self) -> str:
        return self.nom
    
    class Meta:
        #db_table = 'Task'
        verbose_name = _("Tache")
        verbose_name_plural = _("Taches")
        ordering = ['createdAt']
        
class TechnicienTache(models.Model):
    technicien = models.ManyToManyField(Technicien,blank=True)
    #tache = models.ForeignKey(Tache, on_delete=models.CASCADE)

    def __str__(self):
        return self.technicien.nom