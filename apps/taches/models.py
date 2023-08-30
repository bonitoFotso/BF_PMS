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

# Les listes de choix pour les champs avec des choix prédéfinis
prio = [
    ('Bas', 'Bas'),
    ('Moyen', 'Moyen'),
    ('Elever', 'Elever'),
]

jours = [
    ('lundi', 'lundi'),
    ('mardi', 'mardi'),
    ('mercredi', 'mercredi'),
    ('jeudi', 'jeudi'),
    ('vendredi', 'vendredi'),
    ('samedi', 'samedi'),
]



class Tache(models.Model):
    INTERVENTION_CHOICES = [
        ('maintenance', 'Maintenance'),
        ('installation', 'Installation'),
        ('incident', 'Incident'),
        ('survey', 'Survey'),
        ('extension', 'Extension'),
        ('migration', 'Migration'),
    ]

    TYPE_INTERVENTION_CHOICES = [
        ('videosurveillance', 'Vidéosurveillance'),
        ('controle_acces', 'Contrôle d\'accès'),
        ('systeme_incendie', 'Système incendie'),
        ('intrusion', 'Intrusion'),
        ('dab', 'DAB'),
    ]

    STATUS_CHOICES = [
        ('En attente', 'En attente'),
        ('En cours', 'En cours'),
        ('En arrêt', 'En arrêt'),
        ('En facturation', 'En facturation'),
    ]

    nom = models.CharField(_("name"), max_length=50,null=True )
    intervention = models.CharField(choices=INTERVENTION_CHOICES, max_length=20)
    type_intervention = models.CharField(choices=TYPE_INTERVENTION_CHOICES, max_length=20)
    appelant = models.ForeignKey(Appelant, verbose_name=_(" celui qui appelle "), on_delete=models.CASCADE)
    priorite = models.CharField(choices=prio, max_length=20)
    description = models.CharField(max_length=500, null=False, default='description')
    n_OS = models.CharField(_("numero d'OS"), max_length=50, null=True, blank=True)
    ok = models.BooleanField(default=False)
    date_debut = models.DateField(_("date de début"), blank=True, null=True)
    date_fin = models.DateField(_("date de fin"), blank=True, null=True)
    createdAt = models.DateTimeField(auto_now=True)
    updatedAt = models.DateTimeField(auto_now_add=True)
    
    def save(self, *args, **kwargs):
        # Définition du champ "nom" en fonction des valeurs des champs "intervention", "type_intervention" et "createdAt"
        self.nom = f"{self.intervention} - {self.type_intervention} - {self.createdAt}"
        super(Tache, self).save(*args, **kwargs)
        
    def get_agence(self):
        agence = self.appelant.agence
        return agence

    agence = get_agence

    def __str__(self):
        return self.nom

    def update_dates(self, date_debut, date_fin):
        if not self.ok:
            self.date_debut = date_debut
            self.date_fin = date_fin
            self.save()

    def is_done(self):
        return self.ok
    
    def is_active(self):
        return not self.etat or (self.etat.nom != 'En arret' and timezone.now().date() <= self.date_fin)
    
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
    
    def get_taches_attribuees(self):
        return TacheAttribuee.objects.filter(tache=self)

    @property
    def is_overdue(self):
        return self.etat.nom == 'En cours' and timezone.now().date() > self.date_fin

    def is_active(self):
        return not self.etat.exists() or (self.etat.nom != 'En arret' and timezone.now().date() <= self.date_fin)

    class Meta:
        verbose_name = _("Tache")
        verbose_name_plural = _("Taches")
        ordering = ['createdAt']

def update_ok_status(sender, instance, **kwargs):
    # Mise à jour du champ 'ok' de la tâche en fonction des TechnicienTache associés
    technicien_taches = TechnicienTache.objects.filter(tache=instance, ok=True)
    instance.ok = any(technicien_tache.ok for technicien_tache in technicien_taches)
    instance.save()

class TechnicienTache(models.Model):
    technicien = models.ForeignKey(Technicien, verbose_name=_("techniciens"), on_delete=models.CASCADE, blank=True, null=True)
    tache = models.ForeignKey(Tache, on_delete=models.CASCADE)
    ok = models.BooleanField(_("tache effectuer"), default=False)
    date_debut = models.DateField(_("Date de début"), null=True, blank=True)
    date_fin = models.DateField(_("Date de fin"), null=True, blank=True)

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
    technicien_tache = models.ForeignKey(TechnicienTache, verbose_name=_("Tâche effectuée par le technicien"), on_delete=models.CASCADE)
    rapport_text = models.TextField(_("Rapport"))
    date_creation = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Rapport pour {self.technicien_tache.tache.nom} - {self.technicien_tache.technicien.nom}"

class EnregistrementJournalier(models.Model):
    tache = models.ForeignKey(Tache, on_delete=models.CASCADE)
    date = models.DateField()
    description = models.TextField()
    date_import = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.tache} - {self.date}"

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

    class Meta:
        unique_together = (('technicien', 'tache'),)

@receiver(post_save, sender=TechnicienTache)
def create_tache_attribuee(sender, instance, created, **kwargs):
    if created:
        TacheAttribuee.objects.create(technicien=instance.technicien, tache=instance.tache, date_debut=instance.date_debut, date_fin=instance.date_fin)

# Connecter le signal à la fonction de gestionnaire de signal
post_save.connect(create_tache_attribuee, sender=TechnicienTache)

class TacheEffectuee(models.Model):
    technicien = models.ForeignKey(Technicien, verbose_name=_("Technicien"), on_delete=models.CASCADE)
    tache = models.ForeignKey(Tache, verbose_name=_("Tâche effectuée"), on_delete=models.CASCADE)
    date = models.DateField(_("Date d'effectuation"), auto_now_add=True)
    rapport = models.ForeignKey(Rapport, verbose_name=_("Rapport"), on_delete=models.CASCADE, blank=True, null=True)

    def __str__(self):
        return f"{self.technicien.nom} - {self.tache.nom} - {self.date}"

    class Meta:
        unique_together = (('technicien', 'tache'),)

# Mise à jour des statistiques du technicien lors de la création ou de la suppression de TacheAttribuee et TacheEffectuee
@receiver(post_save, sender=TacheAttribuee)
@receiver(pre_delete, sender=TacheAttribuee)
@receiver(post_save, sender=TacheEffectuee)
@receiver(pre_delete, sender=TacheEffectuee)
def update_technicien_stats(sender, instance, **kwargs):
    technicien = instance.technicien
    taches_attribuees = TacheAttribuee.objects.filter(technicien=technicien)
    taches_effectuees = TacheEffectuee.objects.filter(technicien=technicien)

    # Calculer la vitesse d'exécution et l'efficacité et mettre à jour les champs dans le modèle Technicien
    vitesse_execution = len(taches_effectuees) / len(taches_attribuees) if len(taches_attribuees) > 0 else 0.0
    technicien.vitesse_execution = vitesse_execution

    efficacite = len(taches_effectuees) / len(taches_attribuees) if len(taches_attribuees) > 0 else 0.0
    technicien.efficacite = efficacite

    technicien.save()

# Création automatique d'une tâche effectuée lorsqu'un rapport ou TechnicienTache est créé avec ok=True
@receiver(post_save, sender=Rapport)
@receiver(post_save, sender=TechnicienTache)
def create_tache_effectuee(sender, instance, **kwargs):
    if instance.ok and kwargs.get('created', False):
        TacheEffectuee.objects.create(technicien=instance.technicien, tache=instance.tache, rapport=instance)

# Mettre à jour le champ 'ok' de la tâche associée chaque fois qu'une TacheEffectuee est créée
@receiver(post_save, sender=TacheEffectuee)
def update_tache_dates(sender, instance, created, **kwargs):
    if created:
        # Récupérer la tâche effectuée
        tache_effectuee = instance.tache

        # Récupérer tous les TechnicienTache associés à cette tâche
        technicien_taches = TechnicienTache.objects.filter(tache=tache_effectuee)

        # Mettre à jour le champ 'ok' de chaque TechnicienTache associé à True
        for technicien_tache in technicien_taches:
            technicien_tache.ok = True
            technicien_tache.save()
