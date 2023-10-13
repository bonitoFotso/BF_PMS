"""
URL configuration for core project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,include
from django.conf import settings
from django.conf.urls.static import static
import apps.project.models
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('apps.clients.urls')),
    path('', include('apps.project.urls')),
    path('', include('apps.dashboard.urls')),
    path('', include('apps.ressource.urls')),
    path('', include('apps.authentication.urls')),
    #path('', include('apps.adminss.urls')),
    
    path('apil/', include('apps.api_clients.urls')),
    path('api/', include('apps.api.urls')),
]
if bool(settings.DEBUG):
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)