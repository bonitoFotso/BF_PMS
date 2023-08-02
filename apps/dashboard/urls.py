from .views import *
from django.urls import path

urlpatterns = [
    path('',DashView.as_view(),name='dashboards'),
    path('dashboard',HomeView.as_view(),name='dashboard'),
    path('ag',ag,name='ag'),
    path('cir',cir,name='cir'),
#    path('chart', line_chart, name='line_chart'),
#    path('chartJSON', line_chart_json, name='line_chart_json'),
]
