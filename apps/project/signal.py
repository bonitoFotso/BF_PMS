from django.db import models
from django.utils.translation import gettext_lazy as _
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db.models.signals import post_save, pre_save, pre_delete
from django.dispatch import receiver
from apps.clients.models import *
from apps.ressource.models import *
from datetime import date
from datetime import timedelta
from django.utils import timezone
from django.utils.text import slugify
from autoslug import AutoSlugField

from .models import *

@receiver(post_save, sender=Tache)
def create_or_update_enregistrement_journalier(sender, instance, created, **kwargs):
    today = date.today()
    
    try:
        enregistrement = EnregistrementJournalier.objects.get(date=today)
    except EnregistrementJournalier.DoesNotExist:
        enregistrement = EnregistrementJournalier(date=today)
    
    if created:
        enregistrement.taches_creees_count += 1
        enregistrement.tache_totals = Tache.objects.all().count() 
        #enregistrement.tache_att_total = Tache.objects.all().count
        #enregistrement.tache_totals = Tache.objects.all().count
    else:
        try:
            previous_instance = Tache.objects.get(id=instance.id)
            
            if previous_instance.ok != instance.ok:
                enregistrement.taches_effectuees_count += 1
            
            if previous_instance.status == 'En cours':
                enregistrement.taches_attribuees_count += 1
        except Tache.DoesNotExist:
            pass  # Gérer le cas où la tâche précédente n'existe pas
    #enregistrement.tache_totals = enregistrement.taches_creees_count + enregistrement.taches_attribuees_count + enregistrement.taches_effectuees_count
    #enregistrement.tache_att_total = enregistrement.taches_attribuees_count
    #enregistrement.tache_eff_total = enregistrement.taches_effectuees_count
    enregistrement.save()

@receiver(post_save, sender=TechnicienTache)
def create_tache_attribuee(sender, instance, created, **kwargs):
    print('att0 test ',instance)
    if created:
        print('att1 creer',instance)
        TacheAttribuee.objects.create(technicien=instance.technicien, tache=instance.tache, date_debut=instance.date_debut, date_fin=instance.date_fin)
        tache = instance.tache
        tache.date_debut = instance.date_debut
        tache.status = 'En cour'
        tache.save()