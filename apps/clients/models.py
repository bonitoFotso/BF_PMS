from django.db import models
#from apps.authentication.models import User    
from django.utils.translation import gettext_lazy as _
from django.core.validators import MaxValueValidator, MinValueValidator 
from django.db.models.signals import post_save
from django.dispatch import receiver
import datetime


# Create your models here.



class Client(models.Model):
    name = models.CharField(_("name"), max_length=50)
    responsable = models.CharField(_("responsable"), max_length=100)
    email = models.EmailField(_("email"), max_length=254)
    phone = models.CharField(_("phone"), max_length=20)
    address = models.CharField(_("address"), max_length=200)
    city = models.CharField(_("city"), max_length=50)
    n_client = models.CharField(_("numero client"), max_length=50,default='cli_01')
    maintenance = models.BooleanField(_("est sous c. de maintenance"),default=False)
    createdAt = models.DateTimeField(auto_now=True)  # Date de création automatique
    updatedAt = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return '{0}_{1}'.format(self.name,'Siege')
    
    def generate_n_client(self):
        today = datetime.date.today()
        year = today.year
        formatted_name = self.name.replace(" ", "_").upper()  # Convertit le nom en majuscules et remplace les espaces par des underscores
        formatted_city = self.city.replace(" ", "_").upper()  # Convertit la ville en majuscules et remplace les espaces par des underscores
        formatted_date = today.strftime("%Y%m%d")  # Format de date : YYYYMMDD
        generated_n_client = f"{formatted_name}_{formatted_city}_{formatted_date}"
        return generated_n_client

    def save(self, *args, **kwargs):
        if not self.n_client:
            self.n_client = self.generate_n_client()
        super().save(*args, **kwargs)
    
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
    n_agence = models.CharField(_("numero agence"), max_length=50,default='cli_ag_01')
    createdAt = models.DateTimeField(auto_now=True)  # Date de création automatique
    updatedAt = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return '{0}:{1}'.format(self.siege,self.name)
    class Meta:
        verbose_name = _("Agence")
        verbose_name_plural = _("Agences")
        ordering = ['name']
        
    def generate_n_agence(self):
        agence_count = Agence.objects.filter(siege=self.siege).count()
        formatted_n_client = self.siege.n_client.upper()
        generated_n_agence = f"{formatted_n_client}_AG{agence_count+1}"
        return generated_n_agence
    
    def save(self, *args, **kwargs):
        if not self.n_agence:
            self.n_agence = self.generate_n_agence()
        super().save(*args, **kwargs)
        
    @receiver(post_save, sender=Client)
    def create_agence(sender, instance, created, **kwargs):
        if created:
            #generated_n_agence = instance.generate_n_agence()
            
            Agence.objects.create(
                siege=instance,
                name=instance.name,
                responsable=instance.responsable,
                address=instance.address,
                city=instance.city,
                phone=instance.phone,
                email=instance.email,
                #n_agence=generated_n_agence
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

