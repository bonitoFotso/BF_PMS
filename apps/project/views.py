from django.shortcuts import render,redirect
from apps.project.models import  *
from .operation import  pourcent
from apps.clients.models import  *
from django.views.generic import CreateView, DeleteView, UpdateView,DetailView,View,ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.urls import reverse_lazy
from .decorators import manager_required,developer_required
from django.db.models import Q
from django.contrib.auth import get_user_model
User =get_user_model()

#class Task(models.Model):
#    pass

fields = ('date d ajout','agence','appelant','tache','priorite','description','etat','date_debut','technicient','date_fin','n_OS','tec',)
tache_fields = ('agence','appelant','nom','priorite','description','etat','date_debut','technicient',)
# Create your views here.


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
    fields = ('agence','appelant','n_OS','ok','observation','nom','priorite','description','etat','date_debut',)
    success_url = 'task-list'
    
    def get_context_data(self, **kwargs):
        
        ss = self.request.POST
        tt = self.request.GET
        print(ss)
        #print(tt)
        
        context = super().get_context_data(**kwargs)
        context["agences"] = Agence.objects.all()
        context["appelants"] = Appelant.objects.all()
        context["etat"] = Etat.objects.all()
        context["clients"] = Client.objects.all()
        #context["tasks"] = Task.objects.all()
        #context["ta"] =  Task.objects.all().count()
        #context["ta_comp"] =  Task.objects.filter(complete = 'True').count()
        #context["ag"] =  Agence.objects.all().count()
        #context["cl"] =  Client.objects.all().count()
        #context["ag_field"] =  ('name','siege','responsable','email','phone','address','city',)
        #context["cl_field"] =  ('name','responsable','email','phone','address','city',)
        #context["ta_field"] = ('agence', 'title','priority', 'description', 'status', 'complete',)
        context["status"]   = status
        context["pri"]   = prio
        return context


class TacheListView(ListView):
    taches ={}
    ap = []
    model = Tache
    t_f=('tache','tech')
    fields = fields
    p = pourcent(model)
    #a = Tache.objects.all()
    #for i in a:
    #    print(i.appelant.agence)
    #    ap.append(i.appelant.agence)
    tec = TechnicienTache.objects.all()
            
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["app"] = 'Tache'
        context["page"] = 'Liste des Taches'
        context["field"] = self.fields
        context["t_f"] = self.t_f
        context["te"] =  self.tec
        context["taches"]    =  Tache.objects.all().order_by('createdAt')
        context["total"]     =  Tache.objects.count()
        context["complet"]   =  Tache.objects.filter(ok = 'True').count()
        context["incomplet"] =  Tache.objects.filter(ok = 'False').count()
        context["pourcent"] = self.p
        return context


class TaskDetail(DetailView,UpdateView):
    model = Tache
    fields = ('agence','appelant','n_OS','ok','observation','nom','priorite','description','etat','date_debut','date_fin',)
    
    template_name = 'project/tache_detail.html'
    
    success_url = reverse_lazy('task-list')
    
    def get_context_data(self, **kwargs):
        

        
        context = super().get_context_data(**kwargs)
        context["agences"] = Agence.objects.all()
        context["clients"] = Client.objects.all()
        context["appelant"] = Appelant.objects.all()
        context["etat"] = Etat.objects.all()
        #context["tasks"] = Task.objects.all()
        #context["ta"] =  Task.objects.all().count()
        #context["ta_comp"] =  Task.objects.filter(complete = 'True').count()
        #context["ag"] =  Agence.objects.all().count()
        #context["cl"] =  Client.objects.all().count()
        #context["ag_field"] =  ('name','siege','responsable','email','phone','address','city',)
        #context["cl_field"] =  ('name','responsable','email','phone','address','city',)
        #context["ta_field"] = ('agence', 'title','priority', 'description', 'status', 'complete',)
        context["status"]   = status
        context["prio"]   = prio
        return context
    

    



#@method_decorator([login_required(login_url='accounts/login/'),manager_required] , name='dispatch')
class TaskDelete(DeleteView):
    model = Tache
    template_name = 'project/task-delete.html'
    success_url = '/project/dashboard'





class Desk(ListView):
    model = Tache
    template_name = 'project/page-desk.html'
    context_object_name = 'alltask'

    def get(self, request, *args, **kwargs):
        active = Tache.objects.filter( status_id = 1 ) 
        return render(request, self.template_name, {'active': active,'alltask' : Tache.objects.all()})
    


