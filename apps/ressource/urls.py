from django.urls import path, re_path
from .views import *

urlpatterns = [
    path("technicien-create", TechnicienCreateView.as_view(), name="technicien-create"),
    #path("<int:pk>/up", EmployerUpdateView.as_view(), name="emp_upd"),
    #path("<int:pk>/del", EmployerDeleteView.as_view(), name="emp_del"),
    path("technicien-list", TechnicienListView.as_view(), name="technicien-list"),
    path('technicien/<int:pk>/detail',TechnicienDetailView.as_view(),name='technicien-detail'),
    #path('<int:pk>/profile',EmployerProfil.as_view(),name='emp_profile')

]
