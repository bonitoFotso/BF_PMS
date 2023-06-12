from django.contrib import admin
from .models import *

@admin.register(Tache)
class TacheAdmin(admin.ModelAdmin):
    '''Admin View for Tache'''

    list_display = ('nom','agence',)
# Register your models here.
admin.site.register(Etat)
admin.site.register(TechnicienTache)

#admin.site.register(UserTask)

