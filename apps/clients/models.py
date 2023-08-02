from django.db import models
#from apps.authentication.models import User    
from django.utils.translation import gettext_lazy as _
from django.core.validators import MaxValueValidator, MinValueValidator 
from django.db.models.signals import post_save
from django.dispatch import receiver

# Create your models here.

class Client(models.Model):
    name = models.CharField(_("name"), max_length=50)
    responsable = models.CharField(_("responsable"), max_length=100)
    email = models.EmailField(_("email"), max_length=254)
    phone = models.CharField(_("phone"), max_length=20)
    address = models.CharField(_("address"), max_length=200)
    city = models.CharField(_("city"), max_length=50)
    
    def __str__(self):
        return '{0}_{1}'.format(self.name,'Siege')
    class Meta:
        verbose_name = _("Client")
        verbose_name_plural = _("Clients")
        ordering = ['name']
        
        
class Agence(models.Model):
    name = models.CharField(_("name"), max_length=50)
    responsable = models.CharField(_("responsable"), max_length=100)
    address = models.CharField(_("address"), max_length=200)
    city = models.CharField(_("city"), max_length=50)
    siege  = models.ForeignKey("Client", on_delete=models.CASCADE)
    phone = models.CharField(_("phone"), max_length=20)
    email = models.EmailField(_("email"), max_length=254)
    def __str__(self):
        return '{0}:{1}'.format(self.siege,self.name)
    class Meta:
        verbose_name = _("Agence")
        verbose_name_plural = _("Agences")
        ordering = ['name']
        
    @receiver(post_save, sender=Client)
    def create_agence(sender, instance, created, **kwargs):
        if created:
            Agence.objects.create(siege=instance,name = instance.name,
                                responsable = instance.responsable,
                                address = instance.address,
                                city = instance.city,phone = instance.phone,
                                email=instance.email
                                )
            
class Appelant(models.Model):
    name = models.CharField(_("appelant"), max_length=150)
    agence = models.ForeignKey("Agence", verbose_name=_("agence"), on_delete=models.CASCADE)
    addAt = models.DateField(_("ajouter le"), auto_now=False, auto_now_add=True)
    updAt = models.DateField(_("mise a jour le"), auto_now=True, auto_now_add=False)

    def __str__(self):
        return '{0} {1}'.format(self.agence,self.name)
        
    @receiver(post_save, sender=Agence)
    def create_appelant(sender, instance, created, **kwargs):
        if created:
            Appelant.objects.create(name = instance.responsable,agence = instance)

