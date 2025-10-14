from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('ingresar/', views.login_view, name='login'),
    path('crear-cuenta/', views.register_view, name='register'),
    path('app/', views.dashboard, name='dashboard'),
    path('salir/', views.logout_view, name='logout'),
]