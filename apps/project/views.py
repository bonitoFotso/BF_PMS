from django.forms.models import BaseModelForm
from django.http import HttpResponse
from django.shortcuts import render,get_object_or_404,redirect
from apps.project.models import  *
from ajax_datatable.views import AjaxDatatableView
from django.contrib.auth.models import Permission
from .operation import  pourcent
from apps.clients.models import  *
from django.views.generic import CreateView, DeleteView, UpdateView,DetailView,View,ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.urls import reverse_lazy
from .decorators import manager_required,developer_required
from django.db.models import Q
from django.http import JsonResponse

import json
#from apps.ajax_datatable.views import AjaxDatatableView
#from django.contrib.auth.models import Permission

from django.contrib.auth import get_user_model
User =get_user_model()

def is_ajax(request):
    return request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest'

#class Task(models.Model):
#    pass


fields = ('date d ajout','agence','appelant','tache','priorite','description','etat','date_debut','technicient','date_fin','n_OS','tec',)
tache_fields = ('appelant','nom','priorite','description','etat','date_debut','technicient',)
tff = ('appelant','nom','priorite','description','etat','date_debut','technicient',)

# Create your views here.

l = []
def tbb(fi):
    l.append(AjaxDatatableView.render_row_tools_column_def())
    for f in fi:
        t ={'name':f,'visible': True,}
        l.append(t)
    print(l)
    return l
class TacheAjax(AjaxDatatableView):
    model = Tache
    initial_order = [["etat", "asc"], ]
    length_menu = [[-1, 20, 50, 100, -1], [5, 20, 50, 100, 'all']]
    search_values_separator = '+'
    
    column_defs = [
        AjaxDatatableView.render_row_tools_column_def(),
        {'name': 'id', 'visible': False, },
        {'name': 'nom', 'visible': True, },
        #{'name': 'get_agence', 'visible': True, },
        {'name': 'appelant', 'visible': True, },
        {'name': 'priorite', 'visible': True, },
        {'name': 'description', 'visible': True, },
        {'name': 'etat', 'visible': True, },
        {'name': 'date_debut', 'visible': True, },
        {'name': 'technicient','visible': True, },
        {'name': 'n_OS', 'visible': True, },
        {'name': 'date_fin', 'visible': True, },
        
        
        
        #{
        #    'name': 'dow',
        #    'title': 'Action',
        #    'placeholder': True,
        #    'searchable': False,
        #    'orderable': False,
        #    'className': 'highlighted',
        #}, 
        
    ]
    def customize_row(self, row, obj):
        l = []
        for i in obj.technicientache_set.all():
            l.append(i.technicien.nom)
        #days = ['monday', 'tuesday', 'wednesday', 'thyrsday', 'friday', 'saturday', 'sunday']
        print(l)
        row['technicient'] = l# '''%s''' %l
        return


class TaskUpdateView(UpdateView):
    model = Tache
    #template_name = "project/edit_task.html"
    fields = fields
    success_url = reverse_lazy('task-list')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["agences"] = Agence.objects.all()
        context["appelant"] = Appelant.objects.all()
    #    context["clients"] = Client.objects.all()
    #    context["tasks"] = Task.objects.all()
    #    context["ta"] =  Task.objects.all().count()
    #    context["ta_comp"] =  Task.objects.filter(complete = 'True').count()
    #    context["ag"] =  Agence.objects.all().count()
    #    context["cl"] =  Client.objects.all().count()
    #    context["ag_field"] =  ('name','siege','responsable','email','phone','address','city',)
    #    context["cl_field"] =  ('name','responsable','email','phone','address','city',)
    #    context["ta_field"] = ('agence', 'title','priority', 'description', 'status', 'complete',)
        context["status"]   = status
        context["prio"]   = "gsdsdgsd"
        return context

pri = (1,2,3,4,5,6,7,8,9,10)
#@method_decorator([login_required(login_url='accounts/login/'),manager_required] , name='dispatch')
class TaskCreate(CreateView):
    model = Tache
    #template_name = "project/add_task.html"
    fields = ('appelant','n_OS','observation','nom','priorite','description','etat','date_debut',)
    success_url = 'task-list'
    
    def form_valid(self, form: BaseModelForm):
        return super().form_valid(form)
    
    def get_context_data(self, **kwargs):
        print(self.object,'ff')
        context = super().get_context_data(**kwargs)
        context["agences"] = Agence.objects.all()
        context["appelants"] = Appelant.objects.all()
        context["etat"] = Etat.objects.all()
        context["clients"] = Client.objects.all()
        context["status"]   = status
        context["pri"]   = prio
        return context
    
#
def t(request):
    t_list = list(Tache.objects.all().values('nom','priorite','description',))
    return JsonResponse(t_list,safe=False)

class TacheListView(ListView):
    taches ={}
    ap = []
    model = Tache
    t_f=('tache','tech')
    fields = fields
    #t_list = list(Tache.objects.all().values('appelant','n_OS','observation','nom','priorite','description','etat','date_debut',))
    fieldss = ('tache','date d ajout','appelant','priorite','etat','date_debut','technicient','date_fin','n_OS',)
    tec = TechnicienTache.objects.all()

            
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        nb_tasks_bas = Tache.objects.filter(priorite='Bas').count()
        nb_tasks_moyen = Tache.objects.filter(priorite='Moyen').count()
        nb_tasks_elever = Tache.objects.filter(priorite='Elever').count()
        context["app"] = 'Tache'
        context["page"] = 'Liste des Taches'
        context["field"] = self.fieldss
        #context["tl"] = self.s
        context['ass'] = TechnicienTache.objects.all()
        context["taches"]    =  Tache.objects.all().order_by('createdAt')
        context["total"]     =  Tache.objects.count()
        context["ts"]        =  Tache.objects.all()
        context["tech"]      =  Technicien.objects.all()
        context["complet"]   =  Tache.objects.filter(ok = 'True').count()
        context["incomplet"] =  Tache.objects.filter(ok = 'False').count()
        context['nb_tasks_bas'] = nb_tasks_bas
        context['nb_tasks_moyen'] = nb_tasks_moyen
        context['nb_tasks_elever'] = nb_tasks_elever
        context["pourcent"] = pourcent()
        return context



def att(request):
    if request.method == 'POST':
        tec_id = request.POST.get('tec')
        ta_id = request.POST.get('ta')
        
        try:
            tec = get_object_or_404(Technicien, id=tec_id)
            ta = get_object_or_404(Tache, id=ta_id)
        except (ValueError, Technicien.DoesNotExist, Tache.DoesNotExist):
            return JsonResponse({'status': 'error', 'message': 'Invalid technicien or tache ID.'})
        
        try:
            tect = TechnicienTache.objects.create(technicien=tec, tache=ta)
            return JsonResponse({'status': 'success', 'message': 'Attribution successful.'})
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)})
    else:
        return JsonResponse({'status': 'error', 'message': 'Invalid request method.'})


class TaskDetail(DetailView,UpdateView):
    model = Tache
    fields = ('appelant','n_OS','ok','observation','nom','priorite','description','etat','date_debut','date_fin',)
    
    template_name = 'project/tache_detail.html'
    
    success_url = reverse_lazy('task-list')
    
    def get_context_data(self, **kwargs):
        

        
        context = super().get_context_data(**kwargs)
        context["agences"] = Agence.objects.all()
        context["clients"] = Client.objects.all()
        context["appelant"] = Appelant.objects.all()
        context["etat"] = Etat.objects.all()
        context["status"]   = status
        context["prio"]   = prio
        return context
    

    

class EnregistrementJournalierCreateView(CreateView):
    model = EnregistrementJournalier
    template_name = 'enregistrement_journalier_form.html'
    fields = ['tache', 'date', 'description']

    def get_initial(self):
        initial = super().get_initial()
        initial['tache'] = Tache.objects.get(pk=self.kwargs['pk'])  # Pour pré-remplir le champ 'tache'
        return initial

    def get_success_url(self):
        return reverse_lazy('tache-detail', kwargs={'pk': self.kwargs['pk']})


#@method_decorator([login_required(login_url='accounts/login/'),manager_required] , name='dispatch')
class TaskDelete(DeleteView):
    model = Tache
    template_name = 'project/task-delete.html'
    success_url = '/project/dashboard'


class TechnicienTacheUpdateView(UpdateView):
    model = TechnicienTache
    template_name = 'technicien_tache_update.html'
    fields = ['technicien', 'tache', 'ok']

    def get_object(self, queryset=None):
        technicien_tache_id = self.kwargs.get('technicien_tache_id')
        return get_object_or_404(TechnicienTache, pk=technicien_tache_id)

    def form_valid(self, form):
        self.object = form.save()
        response_data = {'success': True}
        return JsonResponse(response_data)

    def form_invalid(self, form):
        response_data = {'success': False, 'errors': form.errors}
        return JsonResponse(response_data, status=400)


class Desk(ListView):
    model = Tache
    template_name = 'project/page-desk.html'
    context_object_name = 'alltask'

    def get(self, request, *args, **kwargs):
        active = Tache.objects.filter( status_id = 1 ) 
        return render(request, self.template_name, {'active': active,'alltask' : Tache.objects.all()})
    
from django.shortcuts import render
from django.http import JsonResponse

from .models import Tache

def create_task(request):
    if request.method == 'POST':
        # Récupérer les données du formulaire
        nom = request.POST.get('nom')
        appelant_id = request.POST.get('appelant')
        priorite = request.POST.get('priorite')
        description = request.POST.get('description')
        n_os = request.POST.get('n_os')
        etat_id = request.POST.get('etat')
        date_debut = request.POST.get('date_debut')
        date_fin = request.POST.get('date_fin')

        # Créer la tâche en base de données
        appelant = Appelant.objects.get(pk=appelant_id)
        etat = Etat.objects.get(pk=etat_id)
        tache = Tache.objects.create(nom=nom, appelant=appelant, priorite=priorite,
                                     description=description, n_OS=n_os, etat=etat,
                                     date_debut=date_debut, date_fin=date_fin)

        # Répondre avec un message de succès
        response_data = {'message': 'Tâche créée avec succès!'}
        return JsonResponse(response_data)
    else:
        # Le formulaire a été soumis de manière incorrecte
        response_data = {'message': 'Erreur lors de la soumission du formulaire'}
        return JsonResponse(response_data, status=400)




class CreateTaskView(CreateView):
    model = Tache
    fields = ['nom', 'appelant', 'priorite', 'description', 'etat',]
    template_name = 'votre_template.html'  # Remplacez "votre_template.html" par le nom de votre modèle

    def get(self, request, *args, **kwargs):
        return JsonResponse({"message": "GET request not supported"})

    def post(self, request, *args, **kwargs):
        print(request.POST)
        form = self.get_form()
        if form.is_valid():
            
            self.object = form.save()
            return JsonResponse({"message": "Tâche créée avec succès!"})
        else:
            
            errors = form.errors.as_json()
            return JsonResponse({"errors": errors}, status=400)

    def get_success_url(self):
        return reverse_lazy("votre_url_de_redirection")  # Remplacez "votre_url_de_redirection" par l'URL où rediriger après la création réussie de la tâche
