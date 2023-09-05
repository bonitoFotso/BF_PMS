# forms.py

from django import forms
from .models import Client, Agence, Appelant

class ClientForm(forms.ModelForm):
    class Meta:
        model = Client
        fields = '__all__'
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control form-control-solid mb-3 mb-lg-0'}),
            'responsable': forms.TextInput(attrs={'class': 'form-control form-control-solid mb-3 mb-lg-0'}),
                 'email': forms.EmailInput(attrs={'class': 'form-control form-control-solid mb-3 mb-lg-0'}),
                  'phone': forms.TextInput(attrs={'class': 'form-control form-control-solid mb-3 mb-lg-0'}),
                'address': forms.TextInput(attrs={'class': 'form-control form-control-solid mb-3 mb-lg-0'}),
                   'city': forms.TextInput(attrs={'class': 'form-control form-control-solid mb-3 mb-lg-0'}),
            'maintenance': forms.CheckboxInput(attrs={'class': 'form-control'}),
        }

class AgenceForm(forms.ModelForm):
    class Meta:
        model = Agence
        fields = '__all__'
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'responsable': forms.TextInput(attrs={'class': 'form-control'}),
            'address': forms.TextInput(attrs={'class': 'form-control'}),
            'city': forms.TextInput(attrs={'class': 'form-control'}),
            'phone': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
        }

class AppelantForm(forms.ModelForm):
    class Meta:
        model = Appelant
        fields = '__all__'
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'agence': forms.Select(attrs={'class': 'form-control'}),
        }
