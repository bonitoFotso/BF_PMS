from django.shortcuts import render
from django.views.generic import CreateView, DeleteView, UpdateView,DetailView,View,ListView,TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from apps.clients.models import *
from apps.ressource.models import *
from apps.project.models import  *
from django.http import JsonResponse
from apps.project.operation import  pourcent
from django.apps import apps
from django.db.models import Count, Avg



from django.contrib.auth.decorators import login_required
#from chartjs.views.lines import BaseLineChartView
# Create your views here.

from datetime import datetime, timedelta
from collections import defaultdict

# Autres imports ...

def submit_data(request):
    if request.method == 'POST':
        # Récupérer les données du formulaire envoyées via AJAX
        id = request.POST.get('id')
        isChecked = request.POST.get('isChecked')
        report = request.POST.get('report')

        # Vérifier que les données nécessaires ont été reçues
        if id is None or isChecked is None or report is None:
            return JsonResponse({'error': 'Invalid data format.'}, status=400)

        # Enregistrer les données dans le modèle Tache ou effectuer toute autre logique de traitement requise
        # Par exemple, vous pouvez créer une nouvelle instance de Tache et l'enregistrer en base de données
        try:
            tache = Tache.objects.get(pk=id)
            tache
            # Autres opérations, si nécessaire...
            return JsonResponse({'message': 'Data submitted successfully!'})
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)

    return JsonResponse({'error': 'Invalid request method.'}, status=405)


def cir(request):
    # Récupérer les tâches effectuées et en cours pour les 7 derniers jours
    today = datetime.today()
    seven_days_ago = today - timedelta(days=7)

    tasks_effectuees = Tache.objects.filter(date_debut__gte=seven_days_ago, ok=True)
    tasks_en_cours = Tache.objects.filter(date_debut__gte=seven_days_ago, ok=False)

    # Créer un dictionnaire pour stocker les données par jour
    data = defaultdict(lambda: {'effectuees': 0, 'en_cours': 0})

    # Compter les tâches effectuées et en cours pour chaque jour
    for task in tasks_effectuees:
        date_str = task.date_debut.strftime('%Y-%m-%d')
        data[date_str]['effectuees'] += 1

    for task in tasks_en_cours:
        date_str = task.date_debut.strftime('%Y-%m-%d')
        data[date_str]['en_cours'] += 1

    # Convertir les données en listes pour le graphique à barres
    dates = list(data.keys())
    effectuees = [data[date]['effectuees'] for date in dates]
    en_cours = [data[date]['en_cours'] for date in dates]

    # Renvoyer les données au format JSON
    return JsonResponse({
        'dates': dates,
        'effectuees': effectuees,
        'en_cours': en_cours,
    })


def ag(request):
    ia = request.GET.get('id')
    a = Client.objects.get(id = ia)
    tab = {}
    client={}
    for d in a.agence_set.all() :
        print(d)
        client={}
        client['id'] = d.id
        client['nom'] = d.name
        client['responsable'] = d.responsable
        client['address'] = d.address
        client['ville'] = d.city
        client['tel'] = d.phone
        client['email'] = d.email
        tab[d.id] = client
    s =a.name
    print(tab)
    return JsonResponse({"a":tab})

class DashView(LoginRequiredMixin,TemplateView):
    template_name = "dashboard/index.html"
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['app'] = "dashboard"
        context["segment"] = 'dashboard'
        #context['taches']    = Technicien.objects.filter(technicien=self.request.user.technicien)
        #context['total']     = Technicien.objects.filter(technicien=self.request.user.technicien).count()
        #context['en_cour']   = Technicien.objects.filter(technicien=self.request.user.technicien).count()
        #context['effectuer'] = Technicien.objects.filter(technicien=self.request.user.technicien).count()

        return context


from dateutil.relativedelta import relativedelta
from datetime import datetime, timedelta

class GroupedBarChartView(View):
    def get(self, request, *args, **kwargs):
        enregistrements = EnregistrementJournalier.objects.all()
        # Créer une liste de dates distinctes en ordre croissant
        dates = sorted(set(enregistrement.date for enregistrement in enregistrements))

        # Générer une séquence continue de dates entre la première et la dernière date
        start_date = dates[0]
        end_date = dates[-1]
        date_sequence = [start_date + timedelta(days=i) for i in range((end_date - start_date).days + 1)]

        # Créer des listes de valeurs pour chaque type de tâche
        taches_creees = [enregistrement.taches_creees_count for enregistrement in enregistrements]
        taches_attribuees = [enregistrement.taches_attribuees_count for enregistrement in enregistrements]
        taches_effectuees = [enregistrement.taches_effectuees_count for enregistrement in enregistrements]

        # Remplir les valeurs manquantes avec 0
        filled_taches_creees = [taches_creees[dates.index(date)] if date in dates else 0 for date in date_sequence]
        filled_taches_attribuees = [taches_attribuees[dates.index(date)] if date in dates else 0 for date in date_sequence]
        filled_taches_effectuees = [taches_effectuees[dates.index(date)] if date in dates else 0 for date in date_sequence]

        data = {
            'labels': [date.strftime('%Y-%m-%d') for date in date_sequence],
            'taches_creees': filled_taches_creees,
            'taches_attribuees': filled_taches_attribuees,
            'taches_effectuees': filled_taches_effectuees,
        }
        
        return JsonResponse(data)





class AnalyseQuantitativeView(View):
    def get(self, request, *args, **kwargs):
        # Récupérer tous les enregistrements journaliers
        enregistrements = EnregistrementJournalier.objects.all()

        # Calculer la séquence de dates entre la première et la dernière date
        dates = sorted(set(enregistrement.date for enregistrement in enregistrements))
        start_date = dates[0]
        end_date = dates[-1]
        date_sequence = [start_date + timedelta(days=i) for i in range((end_date - start_date).days + 1)]

        # Calculer le nombre total de tâches effectuées
        nombre_total_taches_effectuees = Tache.objects.filter(ok=True).count()

        # Calculer le nombre de tâches par type et par intervention
        taches_par_type = Tache.objects.values('type_intervention').annotate(count=Count('id'))
        taches_par_intervention = Tache.objects.values('intervention').annotate(count=Count('id'))
        taches_par_intervention_type = Tache.objects.values('intervention', 'type_intervention').annotate(count=Count('id'))

        # Calculer le nombre de tâches par statut
        nombre_taches_par_statut = Tache.objects.values('status').annotate(count=Count('id'))

        # Calculer le nombre de tâches par technicien
        taches_par_technicien = TechnicienTache.objects.values('technicien__nom').annotate(count=Count('id'))

        # Calculer le nombre de techniciens par tâche
        techniciens_par_tache = TechnicienTache.objects.values('tache__nom').annotate(count=Count('id'))

        # Récupérer les enregistrements journaliers
        enregistrements_journaliers = EnregistrementJournalier.objects.all()

        # Calculer le nombre de tâches effectuées par jour
        taches_effectuees_par_jour = [enreg.taches_effectuees_count for enreg in enregistrements_journaliers]

        # Calculer le nombre de tâches par appelant
        taches_par_appelant = Tache.objects.values('appelant__name').annotate(count=Count('id'))

        # Remplir les valeurs manquantes avec 0
        taches_creees = [enregistrement.taches_creees_count for enregistrement in enregistrements]
        taches_attribuees = [enregistrement.taches_attribuees_count for enregistrement in enregistrements]
        taches_effectuees = [enregistrement.taches_effectuees_count for enregistrement in enregistrements]
        taches_total = [enregistrement.tache_totals for enregistrement in enregistrements]
        
        filled_taches_creees = [taches_creees[dates.index(date)] if date in dates else 0 for date in date_sequence]
        filled_taches_attribuees = [taches_attribuees[dates.index(date)] if date in dates else 0 for date in date_sequence]
        filled_taches_effectuees = [taches_effectuees[dates.index(date)] if date in dates else 0 for date in date_sequence]
        filled_tache_totals = [taches_total[dates.index(date)] if date in dates else 0 for date in date_sequence]

        # Calculer le ratio de tâches par technicien
        try:
            ratio_tache_technicien = len(techniciens_par_tache) / len(taches_par_technicien)
        except ZeroDivisionError:
            ratio_tache_technicien = 0.0  # ou une autre valeur appropriée en cas de division par zéro
        except Exception as e:
            # Gérer d'autres exceptions si nécessaire
            ratio_tache_technicien = 0.0  # ou une autre valeur par défaut en cas d'erreur

        # Construire le dictionnaire de données
        data = {
            'nombre_total_taches_effectuees': nombre_total_taches_effectuees,
            'taches_par_type': list(taches_par_type),
            'nombre_taches_par_statut': list(nombre_taches_par_statut),
            'taches_par_intervention': list(taches_par_intervention),
            'taches_par_intervention_type': list(taches_par_intervention_type),
            'taches_par_technicien': list(taches_par_technicien),
            'techniciens_par_tache': list(techniciens_par_tache),
            'datess': [date.strftime('%Y-%m-%d') for date in date_sequence],
            'dates': [str(enreg.date) for enreg in enregistrements_journaliers],
            'taches_creees_counts': [enreg.taches_creees_count for enreg in enregistrements_journaliers],
            'taches_attribuees_counts': [enreg.taches_attribuees_count for enreg in enregistrements_journaliers],
            'taches_effectuees_counts': [enreg.taches_effectuees_count for enreg in enregistrements_journaliers],
            'ratio_tache_technicien': ratio_tache_technicien,
            'taches_effectuees_par_jour': taches_effectuees_par_jour,
            'taches_par_appelant': list(taches_par_appelant),
            't_cre': filled_taches_creees,
            't_total': filled_tache_totals,
            't_att': filled_taches_attribuees,
            't_eff': filled_taches_effectuees,
        }

        return JsonResponse(data)


class AnalyseQuantitativeTechnicienDetailView(View):
    def get(self, request,pk, *args, **kwargs):
        try:
            technicien = Technicien.objects.get(id=pk)
        except TechnicienTache.DoesNotExist:
            return JsonResponse({'status': 'error', 'message': 'Technician not found.'})

        technicien_data = {
            'technicien': technicien.nom,
        }

        taches_technicien = TechnicienTache.objects.filter(technicien=technicien)

        technicien_data['nombre_taches_effectuees'] = taches_technicien.filter(tache__ok=True).count()
        technicien_data['nombre_taches_attribuees'] = taches_technicien.count()
        technicien_data['vitesse_execution'] = len(taches_technicien.filter(tache__ok=True)) / len(taches_technicien) if len(taches_technicien) > 0 else 0.0
        technicien_data['efficacite'] = len(taches_technicien.filter(tache__ok=True)) / len(taches_technicien) if len(taches_technicien) > 0 else 0.0

        return JsonResponse(technicien_data)

from django.core.exceptions import ObjectDoesNotExist


def get_technicien_task_history(technicien, dates):
    print(dates)
    # Initialiser un dictionnaire par date pour stocker les données
    task_history = defaultdict(lambda: {
        'taches_attribuees': [],
        'taches_effectuees': [],
        'taches_encours': [],
        'nombre_taches_attribuees': 0,
        'nombre_taches_effectuees': 0,
        'nombre_taches_encours': 0,
        'nombre_taches_par_type': defaultdict(int),
        'nombre_taches_par_intervention': defaultdict(int)
    })

    try:
        # Récupérer toutes les tâches attribuées au technicien
        taches_attribuees = TacheAttribuee.objects.filter(technicien=technicien)
        print(taches_attribuees.count())
        for tache_attribuee in taches_attribuees:
            try:
                # Récupérer toutes les tâches effectuées pour la tâche attribuée
                tache_effectuees = TacheEffectuee.objects.filter(tache=tache_attribuee.tache)
                
                for tache_effectuee in tache_effectuees:
                    t_e = tache_effectuee.date
                    if not isinstance(t_e, str):
                        t_e = t_e.strftime('%Y-%m-%d')
                        
                    if t_e is not None:
                        if not isinstance(t_e, str):
                            t_e = t_e.strftime('%Y-%m-%d')
                    else:
                        t_e = ''

                    # Vérifier si la date de la tâche effectuée est dans la liste des dates fournies
                    if t_e in dates:
                        # Mettre à jour les données pour la tâche effectuée
                        task_history[t_e]['taches_effectuees'].append(tache_attribuee.tache)
                        task_history[t_e]['nombre_taches_effectuees'] += 1
                        task_history[t_e]['nombre_taches_encours'] -= 1
                        task_history[t_e]['nombre_taches_par_type'][tache_attribuee.tache.type_intervention] += 1
                        task_history[t_e]['nombre_taches_par_intervention'][tache_attribuee.tache.intervention] += 1
                        #print('a',task_history.items(),'b')
            except ObjectDoesNotExist:
                pass

            # Mettre à jour les données pour la tâche attribuée
            #print('c',task_history,'d')
            dt = tache_attribuee.date_attribuee
            if dt is not None:
                if not isinstance(dt, str):
                    dt = dt.strftime('%Y-%m-%d')
            else:
                dt = ''

            task_history[dt]['taches_attribuees'].append(tache_attribuee.tache)
            task_history[dt]['nombre_taches_attribuees'] += 1
            task_history[dt]['nombre_taches_encours'] += 1
            task_history[dt]['nombre_taches_par_type'][tache_attribuee.tache.type_intervention] += 1
            task_history[dt]['nombre_taches_par_intervention'][tache_attribuee.tache.intervention] += 1
            
    except ObjectDoesNotExist:
        return []

    # Créer la liste finale des données par date
    result = []
    for date, data in task_history.items():
        result.append({
            'date': date,
            'taches_attribuees': [tache.nom for tache in data['taches_attribuees']],
            'nombre_taches_attribuees': data['nombre_taches_attribuees'],
            'taches_effectuees': [tache.nom for tache in data['taches_effectuees']],
            'nombre_taches_effectuees': data['nombre_taches_effectuees'],
            'taches_encours': [tache.nom for tache in data['taches_encours']],
            'nombre_taches_encours': data['nombre_taches_encours'],
            'nombre_taches_par_type': dict(data['nombre_taches_par_type']),
            'nombre_taches_par_intervention': dict(data['nombre_taches_par_intervention']),
        })

    return result


class TechnicienAnalyticsView(View):
    def get(self, request, pk, *args, **kwargs):
        try:
            technicien = Technicien.objects.get(id=1)
        except Technicien.DoesNotExist:
            return JsonResponse({'status': 'error', 'message': 'Technician not found.'})
        
        enregistrements = EnregistrementJournalier.objects.all()

        # Calculer la séquence de dates entre la première et la dernière date
        dates = sorted(set(enregistrement.date for enregistrement in enregistrements))
        start_date = dates[0]
        end_date = dates[-1]
        date_sequence = [start_date + timedelta(days=i) for i in range((end_date - start_date).days + 1)]

        # Récupérer les données spécifiques au technicien
        taches_attribuees_par_type = TacheAttribuee.objects.filter(technicien=technicien).values('tache__type_intervention').annotate(count=Count('id'))
        taches_attribuees_par_intervention = TacheAttribuee.objects.filter(technicien=technicien).values('tache__intervention').annotate(count=Count('id'))

         #Calculer les données pour le graphique en donut
        donut_labels_type = [entry['tache__type_intervention'] for entry in taches_attribuees_par_type]
        donut_data_type = [entry['count'] for entry in taches_attribuees_par_type]
        donut_labels_intervention = [entry['tache__intervention'] for entry in taches_attribuees_par_intervention]
        donut_data_intervention = [entry['count'] for entry in taches_attribuees_par_intervention]
        
        
        # Récupérer les données pour la courbe d'évolution quotidienne
        today = date.today()
        #date_sequence = [today - timedelta(days=i) for i in range(7)]  # Récupérer les 7 derniers jours
        taches_attribuees_par_jour = [TacheAttribuee.objects.filter(technicien=technicien, date_attribuee=date).count() for date in date_sequence]

# Supposons que vous ayez déjà défini technicien et date_sequence

        # Filtrer les tâches attribuées au technicien
        taches_a = TacheAttribuee.objects.filter(technicien=technicien)
        taches_a_list = list(taches_a)
        #print(taches_a_list)
        taches_par_dates = [Tache.objects.filter(ok=True, date_fin=date).count() for date in date_sequence]
        # Créer une liste de listes de tâches pour chaque date dans date_sequence
        taches_par_date = [Tache.objects.filter(ok=True, date_fin=date) for date in date_sequence]
        #print(taches_par_date,'tt',taches_par_dates)
        # Comparer les tâches attribuées avec les tâches pour chaque date
        print(technicien)
        t = []
        for taches_date in taches_par_date:
            for tache in taches_date:
                ts = tache.tacheattribuee_set.all()
                for tss in ts:
                    if tss.technicien == technicien:
                        tes = tss.tache.tacheeffectuee_set.all()
                        for te in tes:
                            
                            t.append(tes)
        
        print(t)
        nombre_taches_effectuees_par_jour = defaultdict(int)

# Parcourir les tâches attribuées pour le technicien
        for taches_date in taches_par_date:
            for tache in taches_date:
                taches_attribuees = TacheAttribuee.objects.filter(technicien=technicien, tache=tache)

                # Parcourir les tâches attribuées pour chaque tâche
                for tache_attribuee in taches_attribuees:
                    taches_effectuees = TacheEffectuee.objects.filter(tache=tache_attribuee.tache)

                    # Parcourir les tâches effectuées pour chaque tâche attribuée
                    for tache_effectuee in taches_effectuees:
                        date_effectuee = tache_effectuee.date.strftime('%Y-%m-%d')
                        nombre_taches_effectuees_par_jour[date_effectuee] += 1
                        
        print(nombre_taches_effectuees_par_jour)

# Maintenant, nombre_taches_effectuees_par_jour contient le nombre de tâches effectuées par jour

        #print(t)
        # Récupérer les données pour la courbe d'évolution de la productivité
        #taches_effectuees_par_jour = [TacheEffectuee.objects.filter(technicien=technicien, date=date).count() for date in date_sequence]

        context = {
            'technicien': technicien.nom,
            'donut_labels_type': donut_labels_type,
            'donut_data_type': donut_data_type,
            'donut_labels_intervention': donut_labels_intervention,
            'donut_data_intervention': donut_data_intervention,
            'date': [date.strftime('%Y-%m-%d') for date in date_sequence],
            #'taches_attribuees_par_jour': taches_attribuees_par_jour,
            #'taches_effectuees_par_jour': taches_effectuees_par_jour,
        }
        
        return JsonResponse(context,safe=False)



class HomeView(LoginRequiredMixin, TemplateView):
    template_name = "dashboard/i.html"
    p = pourcent()
    fields = [
    'nom',
    'intervention/type',
    'Techniciens',
    'appelant',
    'priorite',
    'date_debut',
    'date_fin',
    
]


    ff = ('nom', 'responsable', 'address', )
    
    def get_chart_data(self):
        # Récupérer les tâches effectuées et en cours pour les 7 derniers jours
        today = datetime.today()
        seven_days_ago = today - timedelta(days=7)

        tasks_effectuees = Tache.objects.filter(date_debut__gte=seven_days_ago, ok=True)
        tasks_en_cours = Tache.objects.filter(date_debut__gte=seven_days_ago, ok=False)

        # Créer un dictionnaire pour stocker les données par jour
        data = defaultdict(lambda: {'effectuees': 0, 'en_cours': 0})

        # Compter les tâches effectuées et en cours pour chaque jour
        for task in tasks_effectuees:
            date_str = task.date_debut.strftime('%Y-%m-%d')
            data[date_str]['effectuees'] += 1

        for task in tasks_en_cours:
            date_str = task.date_debut.strftime('%Y-%m-%d')
            data[date_str]['en_cours'] += 1

        # Convertir les données en listes pour le graphique à barres
        dates = list(data.keys())
        effectuees = [data[date]['effectuees'] for date in dates]
        en_cours = [data[date]['en_cours'] for date in dates]

        # Renvoyer les données au format JSON
        return {
            'dates': dates,
            'effectuees': effectuees,
            'en_cours': en_cours,
        }
   

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['app'] = "dashboard"
        context["segment"] = 'dashboard'
        context["clients"] = Client.objects.all()
        #context['tectaches'] = TechnicienTache.objects.all()
        context['taches'] = Tache.objects.all()
        context['ts'] = [10]
        context["complet"] = Tache.objects.filter(ok='True').count()
        context["incomplet"] = Tache.objects.filter(ok='False').count()
        context["pourcent"] = self.p
        context["field"] = self.fields
        context['fields'] = self.ff
        context['interventions'] = Tache.INTERVENTION_CHOICES
        context['type_ints'] = Tache.TYPE_INTERVENTION_CHOICES
        context['status'] = Tache.STATUS_CHOICES
        context["tech"] = Technicien.objects.all()
        context["appelants"] = Appelant.objects.all()
        #context["etats"] = Etat.objects.all()
        #chart_data = self.get_chart_data()
        #context.update(chart_data)
        # Récupérer les données pour le graphique à barres
        return context


from datetime import date

class TechnicienChartsView(TemplateView):
    template_name = 'yourapp/technicien_charts.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        technicien_id = self.kwargs['pk']  # Récupérer l'ID du technicien depuis l'URL
        technicien = Technicien.objects.get(id=technicien_id)
        
        # Récupérer les données pour le graphique en donut
        taches_attribuees_par_type = TacheAttribuee.objects.filter(technicien=technicien).values('tache__type_intervention').annotate(count=Count('id'))
        donut_labels = [entry['tache__type_intervention'] for entry in taches_attribuees_par_type]
        donut_data = [entry['count'] for entry in taches_attribuees_par_type]
        
        # Récupérer les données pour la courbe d'évolution quotidienne
        taches_attribuees_par_jour = TacheAttribuee.objects.filter(technicien=technicien, date_attribuee=date.today()).count()
        
        context['technicien'] = technicien
        context['donut_labels'] = donut_labels
        context['donut_data'] = donut_data
        context['taches_attribuees_par_jour'] = taches_attribuees_par_jour
        
        return context

    

#class LineChartJSONView(BaseLineChartView):
#    def get_labels(self):
#        """Return 7 labels for the x-axis."""
#        return ["January", "February", "March", "April", "May", "Junde"]
#
#    def get_providers(self):
#        """Return names of datasets."""
#        return ["Central", "Eastside", "Westside","ff"]
#
#    def get_data(self):
#        """Return 3 datasets to plot."""
#        tn = TechnicienTache.objects.filter(technicien=self.request.user.technicien).count()
#        return [[tn, 44, 92, 11, 44, 95, 35],
#                [41, 92, 18, 3, 73, 87, 92],
#                [41, 92, 18, 3, 73, 87, 92],
#                [87, 21, 94, 3, 90,]]
        
#line_chart = TemplateView.as_view(template_name='dashboard/i.html')
#line_chart_json = LineChartJSONView.as_view()

