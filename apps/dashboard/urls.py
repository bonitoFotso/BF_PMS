from .views import *
from django.urls import path

urlpatterns = [
    path('',DashView.as_view(),name='dashboard')
]
