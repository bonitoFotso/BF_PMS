from django.contrib.auth import logout
from django.contrib.auth import views as auth_views
from django.contrib.auth.views import LoginView
from django.urls import reverse_lazy
from django.shortcuts import redirect, render, reverse
from django.views.generic import View
import json
from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.contrib.auth import get_user_model

User = get_user_model()
from .forms import (
    LoginForm,
    RegistrationForm,
    UserPasswordChangeForm,
    UserPasswordResetForm,
    UserSetPasswordForm,
)

# Create your views here.
# consumers.py
  


# Authentication
class UserRegisterView(View):
    
    #form_class = RegistrationForm
    #success_url = reverse_lazy('login')
    #template_name = 'accounts/register.html'
    
    def get(self, request):
        return render(request, 'accounts/register.html', {'form': RegistrationForm()})

    def post(self, request):
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form
            user.save()  
            return redirect(reverse('login'))

        return render(request, 'accounts/register.html', {'form': form})
      
def check_user_exists(request):
    email = request.GET.get('email')
    try:
        user = User.objects.get(email=email)
        print(user)
        return JsonResponse({'exists': True})
    
    except User.DoesNotExist:
        return JsonResponse({'exists': False})

#class UserLoginView(auth_views.LoginView):
#  template_name = 'accounts/login.html'
#  success_url = 'profile'

class UserLoginView(LoginView):
    # Spécifie le nom du modèle de template pour la page de connexion
    template_name = 'accounts/log.html'
    form_class = LoginForm
     # Redirige l'utilisateur vers la page de profil si la connexion réussit
    def get_success_url(self):
        return reverse('profile')  # Remplacez par l'URL de la page de profil

    # Vous pouvez également personnaliser davantage le comportement en redéfinissant
    # la méthode `form_valid` pour ajouter des étapes supplémentaires si nécessaire
    #def form_valid(self, form):
    #    # Faites quelque chose ici si nécessaire
    #    return super().form_valid(form)


class UserPasswordResetView(auth_views.PasswordResetView):
  template_name = 'accounts/password_reset.html'
  form_class = UserPasswordResetForm

class UserPasswordResetConfirmView(auth_views.PasswordResetConfirmView):
  template_name = 'accounts/password_reset_confirm.html'
  form_class = UserSetPasswordForm

class UserPasswordChangeView(auth_views.PasswordChangeView):
  template_name = 'accounts/password_change.html'
  form_class = UserPasswordChangeForm

def user_logout_view(request):
  logout(request)
  return redirect('/accounts/login/')


class TechnicienProfileView(LoginRequiredMixin, TemplateView):
    template_name = 'profile.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Ajoutez ici la logique pour récupérer les données du technicien connecté
        context['technicien'] = self.request.user # Assurez-vous que votre modèle User est lié à votre modèle Technicien
        return context
