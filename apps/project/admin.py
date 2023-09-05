from django.contrib import admin
from .models import *

# Administration pour le modèle Categorie
class CategorieAdmin(admin.ModelAdmin):
    list_display = ('nom', 'description', 'createdAt', 'updatedAt')
    list_filter = ('createdAt', 'updatedAt')
    search_fields = ('nom', 'description')
    list_per_page = 10

# Administration pour le modèle Activite
class ActiviteAdmin(admin.ModelAdmin):
    list_display = ('nom', 'description', 'createdAt', 'updatedAt')
    list_filter = ('createdAt', 'updatedAt')
    search_fields = ('nom', 'description', 'projet__nom')
    list_per_page = 10

admin.site.register(Categorie, CategorieAdmin)
admin.site.register(Activite, ActiviteAdmin)

@admin.register(Tache)
class TacheAdmin(admin.ModelAdmin):
    list_display = ('nom','appelant', 'status','activite','categorie', 'n_OS','priorite', 'ok', 'date_debut', 'date_fin')
    list_filter = ('categorie', 'activite', 'appelant', 'priorite', 'ok')
    search_fields = ('nom', 'description')
    date_hierarchy = 'createdAt'
    ordering = ('-createdAt',)

@admin.register(TechnicienTache)
class TechnicienTacheAdmin(admin.ModelAdmin):
    list_display = ('technicien', 'tache', 'ok', 'date_debut', 'date_fin')
    list_filter = ('technicien', 'tache', 'ok')
    search_fields = ('technicien__nom', 'tache__nom')
    date_hierarchy = 'date_debut'
    ordering = ('-date_debut',)

@admin.register(Rapport)
class RapportAdmin(admin.ModelAdmin):
    list_display = ('technicien_tache', 'date_creation')
    list_filter = ('date_creation',)
    search_fields = ('technicien_tache__tache__nom', 'rapport_text')
    date_hierarchy = 'date_creation'
    ordering = ('-date_creation',)

@admin.register(EnregistrementJournalier)
class EnregistrementJournalierAdmin(admin.ModelAdmin):
    list_display = ( 'date', )
    list_filter = ('date',)
    date_hierarchy = 'date'
    ordering = ('-date',)

@admin.register(TacheAttribuee)
class TacheAttribueeAdmin(admin.ModelAdmin):
    list_display = ('technicien', 'tache', 'date_attribuee', 'date_debut', 'date_fin')
    list_filter = ('technicien', 'tache', 'date_attribuee', 'date_debut', 'date_fin')
    search_fields = ('technicien__nom', 'tache__nom')
    date_hierarchy = 'date_attribuee'
    ordering = ('-date_attribuee',)

@admin.register(TacheEffectuee)
class TacheEffectueeAdmin(admin.ModelAdmin):
    list_display = ('tache', 'date', 'rapport')
    list_filter = ('tache', 'date')
    search_fields = ('tache__nom', 'rapport__rapport_text')
    date_hierarchy = 'date'
    ordering = ('-date',)

@admin.register(Action)
class ActionAdmin(admin.ModelAdmin):
    list_display = ('tache','action_type','date',)
    search_fields = ('tache','action_type','date',)
    list_filter = ('tache','action_type','date',)

@admin.register(DonneesTechnicien)
class DonneesTechnicienAdmin(admin.ModelAdmin):
    list_display = ('technicien', 'date', 'taches_attribuees', 'taches_effectuees')
    list_filter = ('technicien', 'date')
    search_fields = ('technicien__nom',)
