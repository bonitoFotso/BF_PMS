from django.contrib import admin
from django.urls import path
from .views import *
from django.contrib.auth.views import LogoutView

urlpatterns = [
    

    #path('dashboard',Dashboard.as_view(),name='dashboard'),
    #path('project-detail/<int:pk>/',ProjectDetail.as_view(),name='projectdetail'),
    #path('project-update/<int:pk>/',ProjectUpdate.as_view(),name='projectupdate'),
    #path('project-delete/<int:pk>/',ProjectDelete.as_view(),name='projectdelete'),

    path('task-list',TacheListView.as_view(),name='task-list'),
    path('task-create',TaskCreate.as_view(),name='task'),
    path('tasks/<int:pk>/edit',TaskUpdateView.as_view(),name='taskupdate'),
    path('tasks/<int:pk>/delete',TaskDelete.as_view(),name='taskdelete'),
    path('tasks/<int:pk>/detail',TaskDetail.as_view(),name='taskdetail'),
    
]
