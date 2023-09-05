from django.urls import path
from .views import *

urlpatterns = [
    path('clients/', ClientView.as_view(), name='clients'),

    path('client-list/', ClientListView.as_view(), name='client-list'),
    path('client-create/', ClientCreateView.as_view(), name='client-create'),
    path('agence-list/', AgenceListView.as_view(), name='agence-list'),
    path('agence-create/', AgenceCreateView.as_view(), name='agence-create'),
    path('appelant-list/', AppelantListView.as_view(), name='appelant-list'),
    path('appelant-create/', AppelantCreateView.as_view(), name='appelant-create'),
    
    
    path('clients_json/', ClientListJson.as_view(), name='client_list_json'),
    path('get_client_data/', get_client_data, name='get_client_data'),

]
