from django.shortcuts import render
from django.views.generic import *
from .models import *
from django.urls import reverse_lazy
# Create your views here.
fieldss = ('nom','prenom','tel','sexe', 'matricule',  'email', )
class TechnicienCreateView(CreateView):
    model = Technicien
    template_name = "ressource/add_techicien.html"
    fields = ('nom','prenom','tel','sexe', 'matricule',  'email', )

    success_url = reverse_lazy('list')
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['app'] = 'Technicien'
        context['segment'] = 'creer'
        return context
#def get_context_data(self, **kwargs):
#        context = super().get_context_data(**kwargs)
#        context["app"] = 'Technicien'
#        context["model"] = 'Technicien'
#        context["page"] = 'Liste des technicien'
#        context["fields"] = fieldss
#        context["technicien"] = Technicien.objects.all()

class TechnicienListView(ListView):
    model = Technicien
    #template_name = ".html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["q"] = 'qq'
        context["app"] = 'Technicien'
        context["model"] = 'Technicien'
        context["page"] = 'Liste des technicien'
        return context
    
    
    
