from django.contrib.auth import views as auth_views
from django.urls import path,re_path
#from . import consumers
from . import views

urlpatterns = [

    # Authentication
    path('accounts/login/', views.UserLoginView.as_view(), name='login'),
    path('accounts/logout/', views.user_logout_view, name='logout'),
    path('accounts/register/', views.UserRegisterView.as_view(), name='register'),
    path('accounts/password-change/', views.UserPasswordChangeView.as_view(), 
         name='password_change'), 
    path('accounts/password-change-done/', auth_views.PasswordChangeDoneView.as_view(
        template_name='accounts/password_change_done.html'
    ), name="password_change_done" ),
    path('accounts/password-reset/', views.UserPasswordResetView.as_view(), 
         name='password_reset'),  
    path('accounts/password-reset-confirm/<uidb64>/<token>/', 
        views.UserPasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('accounts/password-reset-done/', auth_views.PasswordResetDoneView.as_view(
        template_name='accounts/password_reset_done.html'
    ), name='password_reset_done'),
    path('accounts/password-reset-complete/', 
         auth_views.PasswordResetCompleteView.as_view(  
        template_name='accounts/password_reset_complete.html'
    ), name='password_reset_complete'),
    path('profile', views.TechnicienProfileView.as_view(), name='profile'),

    path('check_user_exists/', views.check_user_exists, name='check_user_exists'),

    
]
# routing.py
#websocket_urlpatterns = [
#    re_path(r'ws/online-status/$', consumers.OnlineStatusConsumer.as_asgi()),
#]
