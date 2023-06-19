from django.urls import path
from ajax.views import home, compute

urlpatterns = [
    path('', home, name="home"),
    path('compute/', compute, name="compute"),
]
