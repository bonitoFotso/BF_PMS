from django.shortcuts import render
from django.views.generic import CreateView, DeleteView, UpdateView,DetailView,View,ListView,TemplateView

from apps.clients.models import *
from apps.ressource.models import *
from apps.project.models import  *
# Create your views here.


class DashView(TemplateView):
    template_name = "dashboard/index.html"
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["segment"] = 'dashboard'
        return context
    

    #def get_context_data(self, **kwargs):
    #    context = super().get_context_data(**kwargs)
    #    context["app"] = ''
    #    context["model"] = ''
    #    context["page"] = ''
    #    context["segment"] = 'dashboard'