from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('ingresar/', views.login_view, name='login'),
    path('crear-cuenta/', views.register_view, name='register'),
    path('app/', views.dashboard, name='dashboard'),
    path('salir/', views.logout_view, name='logout'),
    path('ingresar-electrodomestico/', views.ingresar_electrodomestico, name='ingresar_electrodomestico'),
    path('electrodomesticos/', views.listar_electrodomesticos, name='listar_electrodomesticos'),
    path('electrodomesticos/editar/<int:id>/', views.editar_electrodomestico, name='editar_electrodomestico'),
    path('electrodomesticos/eliminar/<int:id>/', views.eliminar_electrodomestico, name='eliminar_electrodomestico'),
    path('calcular-consumos/', views.calcular_consumos, name='calcular_consumos'),
    path("comparar-electrodomesticos/", views.comparar_electrodomesticos, name="comparar_electrodomesticos"),
]