from django.db import models
#from apps.authentication.models import User    
from django.utils.translation import gettext_lazy as _
from django.core.validators import MaxValueValidator, MinValueValidator 
from django.db.models.signals import post_save,pre_save,pre_delete
from django.dispatch import receiver
from apps.clients.models import *
from apps.ressource.models import *
from datetime import date
from datetime import timedelta
from django.utils import timezone

# Create your models here.
prio = [
    ('Bas','Bas'),
    ('Moyen','Moyen'),
    ('Elever','Elever'),
]

jours = [
    ('lundi','lundi'),
    ('mardi','mardi'),
    ('mercredi','mercredi'),
    ('jeudi','jeudi'),
    ('vendredi','vendredi'),
    ('samedi','samedi'),
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
    priorite = models.CharField(choices=prio, max_length=20, )
    description = models.CharField(max_length=500,null=False, default='description')
    n_OS = models.CharField(_("numero d OS"), max_length=50,null=True,blank=True)
    etat = models.ForeignKey("Etat", verbose_name=_("etat"), on_delete=models.CASCADE)
    ok = models.BooleanField(default=False)
    observation = models.CharField(max_length=100, default='observation')
    date_debut = models.DateField(_("date de debut"),blank=True,null=True)
    date_fin = models.DateField(_("date de fin"),blank=True,null=True)
    createdAt = models.DateTimeField(auto_now_add=True)
    updatedAt = models.DateTimeField(auto_now=True)
    def get_agence(self):
        agence = self.appelant.agence
        return agence
    
    agence = get_agence
    
    def __str__(self) -> str:
        return self.nom
    
    def get_progression(self):
        if self.is_active():
            total_days = (self.date_fin - self.date_debut).days
            elapsed_days = (timezone.now().date() - self.date_debut).days
            return min(100, (elapsed_days / total_days) * 100)
        else:
            return 0
        
    @property
    def duree_estimee(self):
        if self.date_debut and self.date_fin:
            return self.date_fin - self.date_debut
        else:
            return timedelta(days=0)
        
    def get_taches_effectuees(self):
        return TacheEffectuee.objects.filter(tache=self)
    
    @property
    def is_overdue(self):
        return self.etat.nom == 'En cours' and timezone.now().date() > self.date_fin

    def is_active(self):
        
        return not self.etat.exists() or (self.etat.nom != 'En arret' and timezone.now().date() <= self.date_fin)
    class Meta:
        #db_table = 'Task'
        verbose_name = _("Tache")
        verbose_name_plural = _("Taches")
        ordering = ['createdAt']
        
        
class TechnicienTache(models.Model):
    technicien = models.ForeignKey(Technicien, verbose_name=_("techniciens"), on_delete=models.CASCADE,blank=True,null=True)
    tache = models.ForeignKey(Tache, on_delete=models.CASCADE)
    ok = models.BooleanField(_("tache effectuer"),default=False)
    #date_fin = models.DateTimeField(auto_now=False, auto_now_add=False,null = 1)
    class Meta:
        unique_together = (('technicien', 'tache'),)
        
    def __str__(self):
        tec = Technicien.objects.get(id=self.technicien_id)
        ta = Tache.objects.get(id=self.tache_id)
        return '%s : %s' % (ta.nom, tec.nom)
    
    @property
    def get_duree(self):
        if self.tache.date_debut and self.tache.date_fin:
            return self.tache.date_fin - self.tache.date_debut
        else:
            return timedelta(days=0)
    

class Rapport(models.Model):
    techtache = models.ForeignKey(TechnicienTache, on_delete=models.CASCADE)
    corp = models.TextField(_("rapport"))
    
    def __str__(self):
        return self.techtache
    
class EnregistrementJournalier(models.Model):
    tache = models.ForeignKey(Tache, on_delete=models.CASCADE)
    date = models.DateField()
    description = models.TextField()
    date_import = models.DateTimeField(auto_now_add=True)  # Nouveau champ pour la date d'importation

    def __str__(self):
        return f"{self.tache} - {self.date}"

# Signal pour créer automatiquement un enregistrement journalier lorsqu'une tâche est mise à jour
@receiver(post_save, sender=Tache)
def create_enregistrement_journalier(sender, instance, **kwargs):
    if instance:
        # Créer un nouvel enregistrement journalier uniquement si la tâche est active
        enregistrement = EnregistrementJournalier(tache=instance, date=date.today(), description="Tâche mise à jour")
        enregistrement.save()

class TacheAttribuee(models.Model):
    technicien = models.ForeignKey(Technicien, verbose_name=_("Technicien"), on_delete=models.CASCADE)
    tache = models.ForeignKey(Tache, verbose_name=_("Tâche attribuée"), on_delete=models.CASCADE)
    date_attribuee = models.DateTimeField(_("Date d'attribution"), auto_now_add=True)
    date_debut = models.DateField(_("Date de début"), null=True, blank=True)
    date_fin = models.DateField(_("Date de fin"), null=True, blank=True)

    def __str__(self):
        return f"{self.technicien.nom} - {self.tache.nom}"
    
def create_tache_attribuee(sender, instance, created, **kwargs):
    if created:
        TacheAttribuee.objects.create(technicien=instance.technicien, tache=instance.tache)

# Connecter le signal à la fonction de gestionnaire de signal
post_save.connect(create_tache_attribuee, sender=TechnicienTache)
class TacheEffectuee(models.Model):
    technicien = models.ForeignKey(Technicien, verbose_name=_("Technicien"), on_delete=models.CASCADE)
    tache = models.ForeignKey(Tache, verbose_name=_("Tâche effectuée"), on_delete=models.CASCADE)
    date = models.DateField(_("Date d'effectuation"),auto_now_add=True)
    # Ajoutez d'autres champs pour les informations supplémentaires sur la tâche effectuée

    def __str__(self):
        return f"{self.technicien.nom} - {self.tache.nom} - {self.date}"
    
@receiver(post_save, sender=TacheAttribuee)
@receiver(pre_delete, sender=TacheAttribuee)
@receiver(post_save, sender=TacheEffectuee)
@receiver(pre_delete, sender=TacheEffectuee)
def update_technicien_stats(sender, instance, **kwargs):
    technicien = instance.technicien
    taches_attribuees = TacheAttribuee.objects.filter(technicien=technicien)
    taches_effectuees = TacheEffectuee.objects.filter(technicien=technicien)

    # Calculez la vitesse d'exécution et l'efficacité et mettez à jour les champs dans le modèle Technicien
    # Exemple de calcul :
    vitesse_execution = len(taches_effectuees) / len(taches_attribuees) if len(taches_attribuees) > 0 else 0.0
    technicien.vitesse_execution = vitesse_execution

    efficacite = len(taches_effectuees) / len(taches_attribuees) if len(taches_attribuees) > 0 else 0.0
    technicien.efficacite = efficacite

    technicien.save()

@receiver(post_save, sender=TechnicienTache)
def create_tache_attribuee(sender, instance, created, **kwargs):
    if created:
        TacheAttribuee.objects.create(technicien=instance.technicien, tache=instance.tache)


post_save.connect(create_tache_attribuee, sender=TechnicienTache)

@receiver(post_save, sender=TechnicienTache)
def create_tache_effectuee(sender, instance, **kwargs):
    if instance.ok and kwargs.get('created', False):
        TacheEffectuee.objects.create(technicien=instance.technicien, tache=instance.tache)

@receiver(post_save, sender=TacheEffectuee)
def update_technicien_taches(sender, instance, **kwargs):
    if kwargs.get('created', False):
        # Récupérer la tâche effectuée
        tache_effectuee = instance.tache

        # Récupérer tous les TechnicienTache associés à cette tâche
        technicien_taches = TechnicienTache.objects.filter(tache=tache_effectuee)

        # Mettre à jour le champ 'ok' de chaque TechnicienTache associé à True
        for technicien_tache in technicien_taches:
            technicien_tache.ok = True
            technicien_tache.save()
