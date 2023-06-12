from django import forms
from .models import  Task

#class TaskForm(forms.ModelForm):
#    class Meta:
#        model = Task
#        fields = '__all__'
#
#        widgets = {
#            'title' : forms.TextInput(attrs={'class' : 'form-control'}),
#            'project' : forms.Select(attrs={'class' : 'form-control'}),
#            'module' : forms.Select(attrs={'class' : 'form-control'}),
#            'priority' : forms.TextInput(attrs={'class' : 'form-control'}),
#            'description' : forms.Textarea(attrs={'class' : 'form-control', 'rows' : 3}),
#            'status' : forms.Select(attrs={'class' : 'form-control'}),
#            'totalMinutes' : forms.NumberInput(attrs={'class' : 'form-control'}),
#        }

