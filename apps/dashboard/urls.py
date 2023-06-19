from .views import *
from django.urls import path

urlpatterns = [
    path('',DashView.as_view(),name='dashboard'),
    path('home',HomeView.as_view(),name='dashboard'),
    path('chart', line_chart, name='line_chart'),
    path('chartJSON', line_chart_json, name='line_chart_json'),
]
