from typing import Any
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render,get_object_or_404,redirect
from django.views.generic import *
from django.contrib.auth.mixins import LoginRequiredMixin
from apps.clients.models import *
from apps.project.models import  *
from .models import *
from django.urls import reverse_lazy
from django.http import JsonResponse
from django_datatables_view.base_datatable_view import BaseDatatableView
# Create your views here.
fieldss = ('nom','prenom', 'matricule','tel','' )

def compute(request):
    print(request.POST)
    a = request.POST.get("a")
    b = request.POST.get("b")
    print(a,b)

    return JsonResponse({"operation_result": int(a) + int(b)})

class Comp(CreateView):
    model = Technicien
    fields = ('nom','prenom','tel', 'matricule',  'email',)
    def post(self, request, *args, **kwargs):
        
        print(request.POST)
        

        return JsonResponse({'data': 'success'})
    def form_valid(self, form):
        response = super().form_valid(form)

class TechnicienCreateView(CreateView):
    model = Technicien
    # template_name = "ressource/add_technicien.html"
    fields = ('nom', 'prenom', 'tel', 'matricule', 'email')
    success_url = reverse_lazy('technicien-list')

    def get(self, request, *args, **kwargs):
        # Vous pouvez ajouter ici du code pour gérer les requêtes GET si nécessaire
        # Par exemple, vous pouvez renvoyer des données supplémentaires sous forme de JSON
        return JsonResponse({"message": "GET request not supported"})

    def post(self, request, *args, **kwargs):
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def form_valid(self, form):
        response = super().form_valid(form)
        return JsonResponse({"message": "Technicien créé avec succès!"})

    def form_invalid(self, form):
        errors = form.errors.as_json()
        return JsonResponse({"errors": errors}, status=400)



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
        #context["att"] = 
        #context["do"] = 
        #context["todo"] = 
        return context
    
    
    
    
class TechnicienDetailView(DetailView,UpdateView):
    model = Technicien
    fields = ('nom','prenom','tel', 'matricule',  'email', )
    template_name = "ressource/technicien_detail.html"
    success_url = reverse_lazy('technicien-list')
    
    def get_stat(self):
        dl = []
        td = []
        att = self.object.technicientache_set.all()
        do = self.object.technicientache_set.all()
        for d in att:
            if d.tache.ok == True:
                dl.append(d.tache)
            else:
                td.append(d)
        stat = {'all':att,"do":dl,"todo":td}
        #print('dd',stat)
        return stat
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        #ss = self.request.POST
        #tt = self.request.GET
        #print(tt)
        # Initialisez votre liste breadcrumb de base
        print(self.object)
        breadcrumb = [{'label': 'Accueil', 'url': '/'}]
        breadcrumb = [{'label': 'Techniciens', 'url': '/technicien-list'}]

        # Ajoutez d'autres éléments au breadcrumb en fonction de la vue actuelle
        
        breadcrumb.append({'label': 'technicien :'+str(self.object.nom), 'url': self.request.path})
        #elif self.request.path == '/autre_page':
        #    breadcrumb.append({'label': 'Autre Page', 'url': '/autre_page'})
        # Ajoutez autant d'éléments que nécessaire en fonction de votre application
        
        # Ajoutez le breadcrumb au contexte
        context['breadcrumb'] = breadcrumb
        
        context["q"] = 'qq'
        context["app"] = 'Technicien'
        context["model"] = 'Technicien'
        context["page"] = 'detail du technicien'
        context["fields"] = fieldss
        context["technicien"] = Technicien.objects.all()
        context["stat"] = self.get_stat()
        #print(context)
        return context
    
class AccountView(LoginRequiredMixin,TemplateView):

    template_name = "accounts/accounts.html"
    

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['app'] = "dashboard"
        context["segment"] = 'dashboard'
        context['taches'] = TechnicienTache.objects.filter(technicien=self.request.user.technicien)
        context['total'] = TechnicienTache.objects.filter(technicien=self.request.user.technicien).count()
        context['en_cour'] = TechnicienTache.objects.filter(technicien=self.request.user.technicien,ok=0).count()
        context['effectuer'] = TechnicienTache.objects.filter(technicien=self.request.user.technicien,ok=1).count()

        return context
    


class TechnicienListJson(BaseDatatableView):
    model = Technicien
    columns = ['id','nom', 'prenom', 'tel', 'email', 'matricule', 'vitesse_execution', 'efficacite']
    order_columns = ['nom', 'prenom', 'tel', 'email', 'matricule', 'vitesse_execution', 'efficacite','id']

    def get_initial_queryset(self):
        return Technicien.objects.all()

    def render_column(self, row, column):
        # Vous pouvez personnaliser le rendu des colonnes ici si nécessaire
        if column == 'vitesse_execution':
            return f"{row.vitesse_execution:.2f}"
        elif column == 'efficacite':
            return f"{row.efficacite:.2f}"
        else:
            return super().render_column(row, column)
