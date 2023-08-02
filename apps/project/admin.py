from django.contrib import admin
from .models import *

@admin.register(Etat)
class EtatAdmin(admin.ModelAdmin):
    list_display = ('nom', 'description', 'motif')

@admin.register(Tache)
class TacheAdmin(admin.ModelAdmin):
    list_display = ('nom', 'appelant', 'priorite', 'etat', 'date_debut', 'date_fin', )
    list_filter = ('priorite', 'etat', )
    search_fields = ('nom', 'appelant__nom', 'appelant__prenom')
    ordering = ('-createdAt',)
    date_hierarchy = 'createdAt'
    #autocomplete_fields = ('appelant',)
    readonly_fields = ('createdAt', 'updatedAt')
    fieldsets = (
        ('Informations générales', {
            'fields': ('nom', 'appelant', 'priorite', 'description', 'n_OS', 'etat', 'observation', 'date_debut', 'date_fin', 'createdAt', 'updatedAt')
        }),
        ('Statut', {
            'fields': ('ok',),
        }),
    )

@admin.register(TechnicienTache)
class TechnicienTacheAdmin(admin.ModelAdmin):
    list_display = ('technicien', 'tache')
    #autocomplete_fields = ('technicien', 'tache')
    def get_queryset(self, request):
        # Override get_queryset to optimize related fields' queryset
        queryset = super().get_queryset(request)
        return queryset.select_related('technicien', 'tache')

    def technicien_display(self, obj):
        return obj.technicien.nom

    def tache_display(self, obj):
        return obj.tache.nom

    technicien_display.short_description = 'Technicien'
    tache_display.short_description = 'Tache'
    

@admin.register(Rapport)
class RapportAdmin(admin.ModelAdmin):
    list_display = ('techtache', 'corp')
    #autocomplete_fields = ('techtache',)
    search_fields = ('techtache__technicien__nom', 'techtache__tache__nom')

@admin.register(EnregistrementJournalier)
class EnregistrementJournalierAdmin(admin.ModelAdmin):
    list_display = ('tache', 'date', 'description', 'date_import')
    list_filter = ('tache',)
    search_fields = ('tache__nom', 'description')
    date_hierarchy = 'date'
    readonly_fields = ('date_import',)

@admin.register(TacheAttribuee)
class TacheAttribueeAdmin(admin.ModelAdmin):
    list_display = ('technicien', 'tache', 'date_attribuee', 'date_debut', 'date_fin')
    list_filter = ('technicien',)
    search_fields = ('technicien__nom', 'technicien__prenom', 'tache__nom')
    date_hierarchy = 'date_attribuee'
    #autocomplete_fields = ('technicien', 'tache')

@admin.register(TacheEffectuee)
class TacheEffectueeAdmin(admin.ModelAdmin):
    list_display = ('technicien', 'tache', 'date')
    list_filter = ('technicien',)
    search_fields = ('technicien__nom', 'technicien__prenom', 'tache__nom')
    date_hierarchy = 'date'
    #autocomplete_fields = ('technicien', 'tache')



