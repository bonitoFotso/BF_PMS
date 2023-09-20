from django.db.models import F
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db.models.signals import post_save, pre_save, pre_delete
from django.db.utils import IntegrityError

from django.dispatch import receiver
from apps.clients.models import *
from apps.ressource.models import *
from datetime import date
from datetime import timedelta
from django.utils import timezone
from django.utils.text import slugify
#importation des signaux personaliser


# Créez un signal personnalisé

class Donnee_jour(models.Model):
    date = models.DateField()



jours = [
    ('lundi', 'lundi'),
    ('mardi', 'mardi'),
    ('mercredi', 'mercredi'),
    ('jeudi', 'jeudi'),
    ('vendredi', 'vendredi'),
    ('samedi', 'samedi'),
]

class Categorie(models.Model):
    nom = models.CharField(max_length=200)
    description = models.TextField()
    createdAt = models.DateTimeField(auto_now=True)  # Date de création automatique
    updatedAt = models.DateTimeField(auto_now_add=True)  # Date de mise à jour automatique
    def __str__(self):
        return self.nom

class Activite(models.Model):
    nom = models.CharField(max_length=200)
    description = models.TextField()
    createdAt = models.DateTimeField(auto_now=True)  # Date de création automatique
    updatedAt = models.DateTimeField(auto_now_add=True)  # Date de mise à jour automatique
    def __str__(self):
        return f"Activité de {self.nom}"
    

class Tache(models.Model):
    # Choix pour le champ 'status'
    STATUS_CHOICES = [
        ('En attente', 'En attente'),
        ('En cours', 'En cours'),
        ('En arrêt', 'En arrêt'),
        ('En facturation', 'En facturation'),
        ('Effectué', 'Effectué'),

    ]
    PRIORITE_CHOICES = [
    ('Bas', 'Bas'),
    ('Moyen', 'Moyen'),
    ('Élevé', 'Élevé'),
]
    activite = models.ForeignKey(Activite, verbose_name=_("Activite"), on_delete=models.CASCADE)
    categorie = models.ForeignKey(Categorie, verbose_name=_("Categorie"), on_delete=models.CASCADE)
    nom = models.CharField(_("intitule"), max_length=200,)
    status = models.CharField(choices=STATUS_CHOICES, max_length=20, default="En attente")  # Choix de statut
    appelant = models.ForeignKey(Appelant, verbose_name=_("Celui qui appelle"), on_delete=models.CASCADE)
    priorite = models.CharField(choices=PRIORITE_CHOICES, max_length=20)  # Choix de priorité
    description = models.CharField(max_length=500, null=False, default='description')
    n_OS = models.CharField(_("Numéro d'OS"), max_length=50, null=True, blank=True)
    ok = models.BooleanField(default=False)  # Champ pour indiquer si la tâche est terminée
    date_debut = models.DateField(_("Date de début"), blank=True, null=True,)
    date_fin     = models.DateField(_("Date de fin"), blank=True, null=True,)
    createdAt = models.DateTimeField(auto_now=True)  # Date de création automatique
    updatedAt = models.DateTimeField(auto_now_add=True,)  # Date de mise à jour automatique

    def save(self, *args, **kwargs):
        # Si la tâche est nouvellement créée et n'a pas encore de date de début, la mettre en "En attente"
        if not self.id and not self.date_debut:
            self.status = 'En attente'
        # Si la tâche a une date de début, la mettre en "En cours"
        elif self.date_debut:
            self.status = 'En cours'
        # Si la tâche a un numéro d'OS, la mettre en "En facturation"
        if self.n_OS:
            self.status = 'En facturation'
        # Si la tâche est marquée comme terminée, la mettre en "Effectué"
        if self.ok:
            self.status = 'Effectué'

        super(Tache, self).save(*args, **kwargs)
        
    def __str__(self):
        return self.nom  # Renvoie le nom unique de la tâche comme représentation en chaîne


    def get_agence(self):
        agence = self.appelant.agence
        return agence

    agence = property(get_agence)



    def update_dates(self, date_debut, date_fin):
        if not self.ok:
            self.date_debut = date_debut
            self.date_fin = date_fin
            self.save()

    def is_done(self):
        return self.ok
    
    def is_active(self):
        return not self.status or (self.status != 'En arret' and timezone.now().date() <= self.date_fin)
    
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
        return self.status == 'En cours' and timezone.now().date() > self.date_fin

    def is_active(self):
        return not self.status.exists() or (self.etat.nom != 'En arret' and timezone.now().date() <= self.date_fin)

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
    createdAt = models.DateTimeField(auto_now=True)  # Date de création automatique

    class Meta:
        unique_together = (('technicien', 'tache'),)

    def __str__(self):
        try:
            tec = self.technicien.nom
            ta = self.tache.nom
            return '%s : %s' % (ta, tec)
        except (Technicien.DoesNotExist, Tache.DoesNotExist):
            return 'TechnicienTache ID: %s' % self.id



    @property
    def get_duree(self):
        if self.tache.date_debut and self.tache.date_fin:
            return self.tache.date_fin - self.tache.date_debut
        else:
            return timedelta(days=0)
        
# Modèle Action



# Modèle EnregistrementJournalier mis à jour



class Rapport(models.Model):
    technicien_tache = models.ForeignKey(TechnicienTache, verbose_name=_("Tâche effectuée par le technicien"), on_delete=models.CASCADE)
    rapport_text = models.TextField(_("Rapport"))
    date_creation = models.DateTimeField(auto_now_add=True)
    technicien_list = models.CharField(_("liste des technicien"), max_length=250,null=True)
    createdAt = models.DateTimeField(auto_now=True)  # Date de création automatique

    def __str__(self):
        return f"Rapport pour {self.technicien_tache.tache.nom} - {self.technicien_tache.technicien.nom}"

class EnregistrementJournalier(models.Model):
    date = models.DateField()
    taches_creees_count = models.PositiveIntegerField(default=0)
    taches_attribuees_count = models.PositiveIntegerField(default=0)
    taches_effectuees_count = models.PositiveIntegerField(default=0)
    tache_totals = models.PositiveIntegerField(default=0)
    tache_att_total = models.PositiveIntegerField(default=0)
    tache_eff_total = models.PositiveIntegerField(default=0)
    createdAt = models.DateTimeField(auto_now=True)  # Date de création automatique

    def __str__(self):
        return f"{self.date}"
    
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
        enregistrement.tache_att_total = Tache.objects.all().count()
        enregistrement.tache_eff_total = Tache.objects.all().count()
    else:
        try:
            taches_effectuees = TacheEffectuee.objects.all()
            taches_effectuees_uniques = set(tache_effectuee.tache for tache_effectuee in taches_effectuees)
            taches_effectuees_filtrees = list(taches_effectuees_uniques)
            
            previous_instance = Tache.objects.get(id=instance.id)
            if previous_instance.ok != instance.ok:
                enregistrement.taches_effectuees_count += 1
            
            if previous_instance.status == 'En cours':
                enregistrement.taches_attribuees_count += 1
        except Tache.DoesNotExist:
            pass  # Gérer le cas où la tâche précédente n'existe pas
    enregistrement.save()



class TacheAttribuee(models.Model):
    technicien = models.ForeignKey(Technicien, verbose_name=_("Technicien"), on_delete=models.CASCADE)
    tache = models.ForeignKey(Tache, verbose_name=_("Tâche attribuée"), on_delete=models.CASCADE)
    date_attribuee = models.DateField(_("Date d'attribution"), auto_now=True)
    date_debut = models.DateField(_("Date de début"), null=True, blank=True)
    date_fin = models.DateField(_("Date de fin"), null=True, blank=True)
    createdAt = models.DateTimeField(auto_now=True)  # Date de création automatique

    def __str__(self):
        return f"{self.technicien.nom} - {self.tache.nom}"

    class Meta:
        unique_together = (('technicien', 'tache'),)


@receiver(post_save, sender=TechnicienTache)
def create_tache_attribuee(sender, instance, created, **kwargs):
    try:
        if created:
            date_attribuee = timezone.now()
            tache_attribuee = TacheAttribuee.objects.create(
                technicien=instance.technicien,
                tache=instance.tache,
                date_attribuee=date_attribuee,
                date_debut=instance.date_debut,
                date_fin=instance.date_fin
            ).save()
            print(f'TacheAttribuee créée pour la tâche {instance.tache.nom}')
    except IntegrityError as e:
        print(f'Erreur lors de la création de TacheAttribuee : {str(e)}')
    except Exception as e:
        print(f'Une erreur s\'est produitess : {str(e)}')
@receiver(post_save, sender=TechnicienTache)
def update_status_tache(sender, instance, created, **kwargs):
    try:
        if created:
            tache = instance.tache
            tache.date_debut = instance.date_debut
            tache.status = 'En cours'
            tache.save()
            print(f'Tache update {instance.tache.nom}')
    except IntegrityError as e:
        print(f'Erreur lors de la maj : {str(e)}')
    except Exception as e:
        print(f'Une erreur s\'est produite : {str(e)}')

# Connecter le signal à la fonction de gestionnaire de signal
class TacheEffectuee(models.Model):
    tache = models.ForeignKey(Tache, verbose_name=_("Tâche effectuée"), on_delete=models.CASCADE)
    date = models.DateField(_("Date d'effectuation"), auto_now_add=True)
    rapport = models.ForeignKey(Rapport, verbose_name=_("Rapport"), on_delete=models.CASCADE, blank=True, null=True)
    createdAt = models.DateTimeField(auto_now=True)  # Date de création automatique

    def __str__(self):
        return f"{self.tache.nom} effectuer le {self.date}"

    def get_team(self):
        try:
            team = TechnicienTache.objects.filter(tache=self.tache)
            return team
        except TechnicienTache.DoesNotExist:
            return []  # Retourner une liste vide en cas d'absence d'équipe
        except Exception as e:
            # Gérer d'autres exceptions si nécessaire
            return None  # Retourner None ou une valeur par défaut en cas d'erreur

    class Meta:
        verbose_name = _("Tâche effectuée")
        verbose_name_plural = _("Tâches effectuées")





@receiver(post_save, sender=Tache)
def create_tache_effectuee(sender, instance, **kwargs):
    if instance.ok:
        tache_effectuee, created = TacheEffectuee.objects.get_or_create(tache=instance)
        if created:
            # Définir d'autres champs si nécessaire
            tache_effectuee.save()
            
@receiver(post_save, sender=TacheEffectuee)
def update_tache_attribuee(sender, instance, created, **kwargs):
    if created:
        # Récupérer toutes les occurrences de TacheAttribuee ayant la même tâche
        Tech_taches = TechnicienTache.objects.filter(tache=instance.tache)
        
        # Mettre à jour le champ 'ok' de toutes les occurrences de TacheAttribuee
        for tech_tache in Tech_taches:
            tech_tache.ok = True
            tech_tache.save()

# Mettre à jour le champ 'ok' de la tâche associée chaque fois qu'une TacheEffectuee est créée
@receiver(post_save, sender=TacheEffectuee)
def update_tache_dates(sender, instance, created, **kwargs):
    if created:
        tache_effectuee = instance.tache
        tache_effectuee.date_fin = instance.date
        tache_effectuee.ok = True
        tache_effectuee.save()
        # Mettre à jour tous les TechnicienTache associés
        TechnicienTache.objects.filter(tache=instance.tache).update(ok=True)

            
class Action(models.Model):
    TACHE_ACTION_CHOICES = [
        ('creation', 'Création'),
        ('attribution', 'Attribution'),
        ('effectuation', 'Effectuation'),
    ]

    tache = models.ForeignKey(Tache, on_delete=models.CASCADE)
    action_type = models.CharField(
        verbose_name=_("Type d'action"),
        choices=TACHE_ACTION_CHOICES,
        max_length=20
    )
    date = models.DateField(_("Date d'action"), auto_now_add=True)
    createdAt = models.DateTimeField(auto_now=True)  # Date de création automatique

    def __str__(self):
        return f"{self.get_action_type_display()} - {self.tache.nom}"

    class Meta:
        verbose_name = _("Action")
        verbose_name_plural = _("Actions")


# Constantes pour les types d'actions
CREATION_ACTION = 'creation'
ATTRIBUTION_ACTION = 'attribution'
EFFECTUATION_ACTION = 'effectuation'


@receiver(post_save, sender=Tache)
def create_tache_action(sender, instance, created, **kwargs):
    if created:
        Action.objects.create(tache=instance, action_type=CREATION_ACTION)


@receiver(post_save, sender=TacheAttribuee)
def create_tache_attribuee_action(sender, instance, created, **kwargs):
    if created:
        Action.objects.create(tache=instance.tache, action_type=ATTRIBUTION_ACTION)


@receiver(post_save, sender=TacheEffectuee)
def create_tache_effectuee_action(sender, instance, created, **kwargs):
    if created:
        Action.objects.create(tache=instance.tache, action_type=EFFECTUATION_ACTION)


class DonneesTechnicien(models.Model):
    technicien = models.ForeignKey(Technicien, on_delete=models.CASCADE)
    date = models.DateField(default=timezone.now)
    taches_attribuees = models.PositiveIntegerField(default=0)
    taches_effectuees = models.PositiveIntegerField(default=0)
    createdAt = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ['technicien', 'date']

    def __str__(self):
        return f"Données pour {self.technicien.nom} le {self.date}"

@receiver(post_save, sender=TacheAttribuee)
@receiver(post_save, sender=TacheEffectuee)
def update_donnees_technicien(sender, instance, **kwargs):
    try:
        technicien = instance.technicien
        date = timezone.now().date()

        donnees, created = DonneesTechnicien.objects.get_or_create(technicien=technicien, date=date)

        if sender == TacheAttribuee:
            donnees.taches_attribuees = TacheAttribuee.objects.filter(technicien=technicien, date_attribuee=date).count()
        elif sender == TacheEffectuee:
            donnees.taches_effectuees = TacheEffectuee.objects.filter(technicien=technicien, date=date).count()

        donnees.save()
    except Exception as e:
        # Gérer l'exception, par exemple, en journalisant l'erreur ou en prenant une autre action appropriée
        pass
