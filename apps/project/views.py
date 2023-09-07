from django.forms.models import BaseModelForm
from django.http import HttpResponse
from django.shortcuts import render,get_object_or_404,redirect
from apps.project.models import  *
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
def tec_ajax(request):
    if request.method == 'POST':
        try:
            nom = request.POST.get('nom')
            prenom = request.POST.get('prenom')
            tel = request.POST.get('tel')
            email = request.POST.get('email')
            photo = request.FILES.get('photo')

            # Votre logique de validation et traitement ici
            if nom and prenom and tel and email and photo:
                # Sauvegarde des données dans le modèle Technicien
                technicien = Technicien(nom=nom, prenom=prenom, tel=tel, email=email, photo=photo)
                technicien.save()
                print('success')
                return JsonResponse({'success': True})
            else:
                return JsonResponse({'success': False, 'message': 'Veuillez remplir tous les champs.'})

        except Exception as e:
            return JsonResponse({'success': False, 'message': f'Une erreur s\'est produite : {str(e)}'})


fields = ('date d ajout','agence','appelant','tache','priorite','description','etat','date_debut','technicient','date_fin','n_OS','tec',)
tache_fields = ('appelant','nom','priorite','description','etat','date_debut','technicient',)
tff = ('appelant','nom','priorite','description','etat','date_debut','technicient',)

# Create your views here.

l = []


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
        #context["status"]   = status
        context["prio"]   = "gsdsdgsd"
        return context

pri = (1,2,3,4,5,6,7,8,9,10)
#@method_decorator([login_required(login_url='accounts/login/'),manager_required] , name='dispatch')
class TaskCreate(CreateView):
    model = Tache
    #template_name = "project/add_task.html"
    fields = [
    'nom',
    'appelant',
    'priorite',
    'description',
    'n_OS',
    'date_debut',
    'date_fin',
    
]
    success_url = 'task-list'
    
    def form_valid(self, form: BaseModelForm):
        return super().form_valid(form)
    
    def get_context_data(self, **kwargs):
        print(self.object,'ff')
        context = super().get_context_data(**kwargs)
        context["agences"] = Agence.objects.all()
        context["appelants"] = Appelant.objects.all()
        context["clients"] = Client.objects.all()
        #context["pri"]   = prio
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
    fieldss = ('tache','date d ajout','appelant','priorite','status','date_debut','technicient','date_fin','n_OS',)
    #tec = TechnicienTache.objects.all()

            
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        breadcrumb = [{'label': 'Accueil', 'url': '/'}]  # Le breadcrumb de base
        breadcrumb.append({'label': 'Client', 'url': '/clients'})  # Ajoutez les éléments au breadcrumb
        #request.breadcrumb = breadcrumb  # Ajoutez le breadcrumb au contexte
        
        nb_tasks_bas = Tache.objects.filter(priorite='Bas').count()
        nb_tasks_moyen = Tache.objects.filter(priorite='Moyen').count()
        nb_tasks_elever = Tache.objects.filter(priorite='Elever').count()
        context["app"] = 'Tache'
        context["page"] = 'Liste des Taches'
        context["field"] = self.fieldss
        #context["tl"] = self.s
        #context['ass'] = TechnicienTache.objects.all()
        context["cats"] = Categorie.objects.all()
        context["acts"] = Activite.objects.all()

        context["agences"] = Agence.objects.all()
        context["appelants"] = Appelant.objects.all()
        context["clients"] = Client.objects.all()
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



# views.py
def get_task_info(request):
    task_id = request.GET.get('task_id')
    try:
        task = Tache.objects.get(id=task_id)
        task_info = {
            'id': task.id,
            'nom': task.nom,
            'appelant': task.appelant.name,
            'client' : task.appelant.agence.siege.name,
            'priorite': task.priorite,
            'description': task.description,
            'activite': task.activite.nom,
            'categorie': task.categorie.nom,
            'n_os': task.n_OS,
            'status': task.status,
            'date_debut': task.date_debut.strftime('%Y-%m-%d') if task.date_debut else None,
            'date_fin': task.date_fin.strftime('%Y-%m-%d') if task.date_fin else None,
            # Ajoutez d'autres champs ici
        }
        return JsonResponse({'task_info': task_info})
    except Tache.DoesNotExist:
        return JsonResponse({'error': 'Tâche non trouvée'}, status=404)


def att(request):
    if request.method == 'POST':
        tec_id = request.POST.get('tec')
        ta_id = request.POST.get('ta')
        date_debut = request.POST.get('date_debut')
        date_fin = request.POST.get('date_fin')
        
        try:
            tec = get_object_or_404(Technicien, id=tec_id)
            ta = get_object_or_404(Tache, id=ta_id)
        except (ValueError, Technicien.DoesNotExist, Tache.DoesNotExist):
            return JsonResponse({'status': 'error', 'message': 'ID de technicien ou de tâche invalide.'})
        
        try:
            print('try1,test')
            # Vérifier si la tâche est déjà accomplie
            if ta.ok:
                print('try1,ok')
                return JsonResponse({'status': 'error', 'message': 'La tâche est déjà accomplie et ne peut pas être attribuée à un nouveau technicien.'})
            
            # Vérifier si la tâche est déjà attribuée à un technicien avec ok=True
            existing_tech_tache = TechnicienTache.objects.filter(tache=ta, technicien=tec)
            
            if existing_tech_tache:
                # La tâche est déjà attribuée, donc mettez à jour uniquement la date de début
                existing_tech_tache = existing_tech_tache.first()  # Prendre le premier résultat
                existing_tech_tache.date_debut = date_debut
                existing_tech_tache.date_fin = date_fin
                existing_tech_tache.save()
                print('if2,ok')
            else:
                
                TechnicienTache.objects.create(technicien=tec, tache=ta, date_debut=date_debut, date_fin=date_fin)
                print('else2,ok')
            return JsonResponse({'status': 'success', 'message': 'Attribution réussie.'})
        
        except Exception as e:
            print(str(e))
            return JsonResponse({'status': 'error', 'message': str(e)})
    else:
        return JsonResponse({'status': 'error', 'message': 'Méthode de requête invalide.'})



def edit_task(request):
    if request.method == 'POST':
        ta_id = request.POST.get('ta_id')
        task_done = request.POST.get('task_done') == 'true'  # Convertir en booléen

        num_os = request.POST.get('num_os')
        rapport_text = request.POST.get('rapport_text')

        try:
            ta = get_object_or_404(Tache, id=ta_id)
            tt = ta.technicientache_set.first()

            if ta.ok:
                return JsonResponse({'status': 'error', 'message': 'La tâche est déjà accomplie et ne peut pas être modifiée.'})
            
            if tt:
                tt.ok = task_done
                tt.save()

            # Mettre à jour les champs de la tâche
            ta.n_OS = num_os
            ta.save()

            # Créer un nouveau rapport
            t_list = ta.technicientache_set.all()
            tl = [technicien_tache.technicien.nom for technicien_tache in t_list]
            rapport = Rapport.objects.create(technicien_tache=tt, rapport_text=rapport_text, technicien_list=tl)
            
            return JsonResponse({'status': 'success', 'message': 'Tâche modifiée avec succès.', 'techniciens': tl})
        except Tache.DoesNotExist:
            return JsonResponse({'status': 'error', 'message': 'ID de tâche invalide.'})
        except Exception as e:
            print(e)
            return JsonResponse({'status': 'error', 'message': 'Une erreur s\'est produite lors de la modification de la tâche.'})
    else:
        return JsonResponse({'status': 'error', 'message': 'Méthode de requête invalide.'})


class TaskDetail(DetailView,UpdateView):
    model = Tache
    fields = ('appelant','n_OS','ok','nom','priorite','description','date_debut','date_fin',)
    
    template_name = 'project/tache_detail.html'
    
    success_url = reverse_lazy('task-list')
    
    def get_context_data(self, **kwargs):
        

        
        context = super().get_context_data(**kwargs)
        context["agences"] = Agence.objects.all()
        context["clients"] = Client.objects.all()
        context["appelant"] = Appelant.objects.all()
        #context["etat"] = Etat.objects.all()
        #context["status"]   = status
        #context["prio"]   = prio
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
    


def create_task(request):
    if request.method == 'POST':
        # Récupérer les données du formulaire
        nom = request.POST.get('nom')
        appelant_id = request.POST.get('appelant')
        priorite = request.POST.get('priorite')
        description = request.POST.get('description')
        n_os = request.POST.get('n_os')
        #date_debut = request.POST.get('date_debut')
        #date_fin = request.POST.get('date_fin')
        # Créer la tâche en base de données
        appelant = Appelant.objects.get(pk=appelant_id)
        #etat = Etat.objects.get(pk=etat_id)
        tache = Tache.objects.create( appelant=appelant, priorite=priorite,
                                     description=description, n_OS=n_os,)
                                    # date_debut=date_debut, date_fin=date_fin)

        # Répondre avec un message de succès
        response_data = {'message': 'Tâche créée avec succès!'}
        return JsonResponse(response_data)
    else:
        # Le formulaire a été soumis de manière incorrecte
        response_data = {'message': 'Erreur lors de la soumission du formulaire'}
        return JsonResponse(response_data, status=400)

def create_appelant(request):
    if request.method == 'POST':
        nom_appelant = request.POST.get('nom_appelant')
        if nom_appelant:
            appelant = Appelant.objects.create(name=nom_appelant)
            return JsonResponse({'message': f"L'appelant '{appelant.name}' a été créé avec succès."})
        else:
            return JsonResponse({'errors': 'Le nom de l\'appelant ne peut pas être vide.'}, status=400)
    return redirect('/')

# Autres vues existantes ...




class CreateTaskView(CreateView):
    model = Tache
    fields = [
        'nom',
        'categorie',
        'activite',
        'appelant',
        'priorite',
        'description',
        'n_OS',
        'date_debut',
        'date_fin'
    ]
    template_name = 'votre_template.html'

    def get(self, request, *args, **kwargs):
        return JsonResponse({"message": "Les requêtes GET ne sont pas prises en charge."}, status=405)  # Méthode non autorisée

    def post(self, request, *args, **kwargs):
        form = self.get_form()
        if form.is_valid():
            self.object = form.save()
            return JsonResponse({"message": "Tâche créée avec succès!"})
        else:
            errors = form.errors.as_json()
            return JsonResponse({"errors": errors}, status=400)

    def get_success_url(self):
        # Remplacez "votre_url_de_redirection" par l'URL où rediriger après la création réussie de la tâche
        return reverse_lazy("votre_url_de_redirection", kwargs={"pk": self.object.pk})  # Exemple de redirection avec la clé primaire de la tâche
