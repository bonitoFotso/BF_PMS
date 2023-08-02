from django.shortcuts import render
from ajax_datatable.views import AjaxDatatableView
from django.views.generic import *
from django.urls import reverse_lazy
from .models import *
from django.http import JsonResponse

# Register your models here.
ff = ('nom', 'responsable','address', )

class AgenceAjax(AjaxDatatableView):
    model = Agence
    
    initial_order = [["name", "asc"], ]
    length_menu = [[5, 20, 50, 100, -1], [5, 20, 50, 100, 'all']]
    search_values_separator = '+'

    column_defs = [
        AjaxDatatableView.render_row_tools_column_def(),
        {'name': 'id', 'visible': True, },
        {'name': 'name', 'visible': True, },
        {'name': 'responsable', 'visible': True, },
        
        {
            'name': 'dow',
            'title': 'Action',
            'placeholder': True,
            'searchable': False,
            'orderable': False,
            'className': 'highlighted',
        }, 
        
    ]
    
    def customize_row(self, row, obj):
        #days = ['monday', 'tuesday', 'wednesday', 'thyrsday', 'friday', 'saturday', 'sunday']
        
        row['dow'] = ''' <div class=" list-action">
                                <a href="/agence/%s/detail" class="mr-5" data-toggle="tooltip" data-kt-menu-placement="bottom-end" title="" data-original-title="View"
                                    href="#"><i class="fas fa-eye mr-0"></i></a>
                            </div>''' %obj.pk
        return

class ClientListView(ListView):
    model = Client
    template_name = "clients/list_client.html"
    def get_context_data(self, **kwargs):
        
        context = super().get_context_data(**kwargs)
        context["client"] = Client.objects.all()
        context["agences"] = 2 #Agence.objects.filter(id=self.request.objects.id)
        context['field'] = ff
        return context
    
class AgenceListView(ListView):
    model = Agence
    template_name = "clients/list_agence.html"
    def get_context_data(self, **kwargs):
        
        context = super().get_context_data(**kwargs)
        context["agences"] = Agence.objects.all()
        context["clients"] = Client.objects.all()
        #context["agences"] = 2#Agence.objects.filter(id=self.request.objects.id)
        context['field'] = ff
        return context
    
class ClientDetaiView(DetailView):
    model = Client
    template_name = "clients/detail_client.html"
    def get_context_data(self, **kwargs):
        s = Agence.objects.filter(id=self.object.id)
        print(s)
        context = super().get_context_data(**kwargs)
        context["client"] = Client.objects.all()
        context["agences"] = Agence.objects.all().filter(siege=self.object.id)
        context['field'] = ff
        return context
    
class AgenceDetaiView(DetailView):
    model = Agence
    template_name = "clients/detail_agence.html"
    def get_context_data(self, **kwargs):
        s = Agence.objects.filter(id=self.object.id)
        print(s)
        context = super().get_context_data(**kwargs)
        context["Agences"] = Agence.objects.all()
        #context["agences"] = Agence.objects.all().filter(siege=self.object.id)
        context['field'] = ff
        return context

class ClientCreateView(CreateView):
    model = Client
    fields = ['name', 'responsable','email','phone','address','city']
    template_name = 'clients/client_form.html'
    success_url = reverse_lazy('client-list')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["clients"]   =  Client.objects.order_by('-id') 
        #context["clientss"]  =  Client.objects.filter(isCompleted = 'True').values().count
        context['client']    =  Client.objects.count()
        context['page']      = 'client'
        context['fields']      = ff
        return context
    
    
class ClientUpdateView(UpdateView):
    model = Client
    fields = ['name',]# 'responsable','email','phone','address','city' ]
    template_name = 'clients/client.html'
    success_url = reverse_lazy('client')
    
    
class ClientDeleteView(DeleteView):
    model = Client
    fields = ('name', 'responsable','email','phone','address','city' )
    template_name = 'clients/client.html'
    success_url = reverse_lazy('client')
    
    

class AgenceCreateView(CreateView):
    model = Agence
    fields = ('name', 'responsable','email','phone','address','city','siege' )
    #template_name = 'clients/agence_form.html'
    success_url = reverse_lazy('agence')
        
    def get(self, request, *args, **kwargs):
        return JsonResponse({"as": 12})
    
    
    def post(self, request, *args, **kwargs):
        print(request.POST)
        return super().post(request, *args, **kwargs)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["agences"]   =  Agence.objects.order_by('-id') 
        #context["agencess"]  =  Agence.objects.filter(isCompleted = 'True').values().count
        context['agence']    =  Agence.objects.count()
        context['page']      = 'agence'
        return context

    
class AgenceUpdateView(UpdateView):
    model = Agence
    fields = ('name', 'responsable','email','phone','address','city','siege' )
    template_name = 'clients/agence.html'
    success_url = reverse_lazy('agence')
    
    
class AgenceDeleteView(DeleteView):
    model = Agence
    fields = ('name', 'responsable','email','phone','address','city','siege' )
    template_name = 'clients/agence.html'
    success_url = reverse_lazy('agence')