from django.shortcuts import render
from django.views.generic import CreateView, DeleteView, UpdateView,DetailView,View,ListView,TemplateView

# Create your views here.


class DashView(TemplateView):
    template_name = "dashboard/index.html"
