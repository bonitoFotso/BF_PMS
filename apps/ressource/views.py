from django.shortcuts import render
from django.views.generic import *
from .models import *
from django.urls import reverse_lazy
# Create your views here.
fieldss = ('nom','prenom','tel','sexe', 'matricule',  'email', )
class TechnicienCreateView(CreateView):
    model = Technicien
    #template_name = "ressource/add_techicien.html"
    fields = ('nom','prenom','tel', 'matricule',  'email','user')

    success_url = reverse_lazy('technicien-list')
    def get_context_data(self, **kwargs):
        
        ss = self.request.POST
        tt = self.request.GET
        print(ss)
        
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
        context["fields"] = fieldss
        context["technicien"] = Technicien.objects.all()
        return context
    
    
class TechnicienDetailView(DetailView,UpdateView):
    model = Technicien
    fields = ('nom','prenom','tel', 'matricule',  'email', )
    template_name = "ressource/technicien_detail.html"
    success_url = reverse_lazy('technicien-list')
    def get_context_data(self, **kwargs):
        
        ss = self.request.POST
        tt = self.request.GET
        print(tt)
        
        context = super().get_context_data(**kwargs)
        context["q"] = 'qq'
        context["app"] = 'Technicien'
        context["model"] = 'Technicien'
        context["page"] = 'detail du technicien'
        context["fields"] = fieldss
        context["technicien"] = Technicien.objects.all()
        return context


