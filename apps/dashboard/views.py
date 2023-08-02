from django.shortcuts import render
from django.views.generic import CreateView, DeleteView, UpdateView,DetailView,View,ListView,TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from apps.clients.models import *
from apps.ressource.models import *
from apps.project.models import  *
from django.http import JsonResponse
from apps.project.operation import  pourcent


from django.contrib.auth.decorators import login_required
#from chartjs.views.lines import BaseLineChartView
# Create your views here.

def cir(request):
    ta = Tache.objects.all()
    d = [1,8,6,7,5,4]
    l = ['a','b','c']
    a = {'data':d,'label':l}
    return JsonResponse(a)
    

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
        context['taches'] = TechnicienTache.objects.filter(technicien=self.request.user.technicien)
        context['total'] = TechnicienTache.objects.filter(technicien=self.request.user.technicien).count()
        context['en_cour'] = TechnicienTache.objects.filter(technicien=self.request.user.technicien).count()
        context['effectuer'] = TechnicienTache.objects.filter(technicien=self.request.user.technicien).count()

        return context

    
class HomeView(LoginRequiredMixin,TemplateView):
    template_name = "dashboard/i.html"
    p = pourcent()
    fieldss = ('tache','date d ajout','appelant','priorite','etat','date_debut','technicient','date_fin','n_OS',)
    ff = ('nom', 'responsable','address', )
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['app'] = "dashboard"
        context["segment"] = 'dashboard'
        context["clients"] = Client.objects.all()
        context['tectaches'] = TechnicienTache.objects.all()
        context['taches'] = Tache.objects.all()
        context['ts'] = [10]
        context["complet"]   =  Tache.objects.filter(ok = 'True').count()
        context["incomplet"] =  Tache.objects.filter(ok = 'False').count()
        context["pourcent"] = self.p
        context["field"] = self.fieldss
        context['fields'] = self.ff
        context["tech"]      =  Technicien.objects.all()
        context["appelants"] = Appelant.objects.all()
        context["etats"] = Etat.objects.all()
        


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

