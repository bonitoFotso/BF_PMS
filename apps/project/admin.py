from django.contrib import admin
from django.contrib.admin import AdminSite
from .models import *

@admin.register(Tache)
class TacheAdmin(admin.ModelAdmin):
    '''Admin View for Tache'''

    list_display = ('nom','agence',)
# Register your models here.
admin.site.register(Etat)
admin.site.register(TechnicienTache)

#admin.site.register(UserTask)

admin.site.register(TacheTime)

class TacheTimeInline(admin.TabularInline):
    model = TacheTime
    extra = 0


