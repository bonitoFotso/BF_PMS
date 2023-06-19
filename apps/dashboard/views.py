from django.shortcuts import render
from django.views.generic import CreateView, DeleteView, UpdateView,DetailView,View,ListView,TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from apps.clients.models import *
from apps.ressource.models import *
from apps.project.models import  *
from django.contrib.auth.decorators import login_required
from chartjs.views.lines import BaseLineChartView
# Create your views here.


class DashView(LoginRequiredMixin,TemplateView):
    template_name = "dashboard/index.html"
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['app'] = "dashboard"
        context["segment"] = 'dashboard'
        context['taches'] = TechnicienTache.objects.filter(technicien=self.request.user.technicien)
        context['tn'] = TechnicienTache.objects.filter(technicien=self.request.user.technicien).count()
        return context
    
    
class HomeView(TemplateView):
    template_name = "dashboard/i.html"
    

class LineChartJSONView(BaseLineChartView):
    def get_labels(self):
        """Return 7 labels for the x-axis."""
        return ["January", "February", "March", "April", "May", "Junde"]

    def get_providers(self):
        """Return names of datasets."""
        return ["Central", "Eastside", "Westside","ff"]

    def get_data(self):
        """Return 3 datasets to plot."""
        tn = TechnicienTache.objects.filter(technicien=self.request.user.technicien).count()
        return [[tn, 44, 92, 11, 44, 95, 35],
                [41, 92, 18, 3, 73, 87, 92],
                [41, 92, 18, 3, 73, 87, 92],
                [87, 21, 94, 3, 90,]]
        
line_chart = TemplateView.as_view(template_name='dashboard/i.html')
line_chart_json = LineChartJSONView.as_view()

