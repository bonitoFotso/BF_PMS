from django.contrib import admin
from .models import Client, Agence, Appelant

@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = ('name', 'responsable', 'email', 'phone', 'city', 'n_client', 'maintenance')
    search_fields = ('name', 'responsable', 'n_client')

@admin.register(Agence)
class AgenceAdmin(admin.ModelAdmin):
    list_display = ('name', 'responsable', 'siege', 'city', 'n_agence')
    list_filter = ('siege',)
    search_fields = ('name', 'responsable', 'n_agence')

@admin.register(Appelant)
class AppelantAdmin(admin.ModelAdmin):
    list_display = ('name', 'agence', 'addAt', 'updAt')
    list_filter = ('agence',)
    search_fields = ('name',)