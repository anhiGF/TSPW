"""
URL configuration for tutorias_itsj project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
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
from django.urls import include, path
from django.contrib.auth import views as auth_views
from gestion_tutorias import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('admin/', admin.site.urls),
    path('', views.landing, name='landing'),
    path('registro/', views.registro, name='registro'),
    path('login/', auth_views.LoginView.as_view(template_name='gestion_tutorias/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('dashboard/', views.dashboard, name='dashboard'),
    
    # Restablecimiento de contraseña
    path('password-reset/',
         auth_views.PasswordResetView.as_view(
             template_name='gestion_tutorias/password_reset.html'
         ),
         name='password_reset'),
         
    path('password-reset/done/',
         auth_views.PasswordResetDoneView.as_view(
             template_name='gestion_tutorias/password_reset_done.html'
         ),
         name='password_reset_done'),

    path('password-reset-confirm/<uidb64>/<token>/',
         auth_views.PasswordResetConfirmView.as_view(
             template_name='gestion_tutorias/password_reset_confirm.html'
         ),
         name='password_reset_confirm'),

    path('password-reset-complete/',auth_views.PasswordResetCompleteView.as_view( template_name='gestion_tutorias/password_reset_complete.html' ), name='password_reset_complete'),

          path('captcha/', include('captcha.urls')),
]
