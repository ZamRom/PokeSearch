# Librerías y modulos
from django.urls import path
from . import views

# Rutas de las vistas de la aplicación
urlpatterns = [
    path('', views.inicio, name='home'),
    path('project/', views.pokemon, name='pokemon'),
    path('buscar/', views.buscar_pokemon, name='buscar_pokemon'),
    path('pokemon/<str:pokemon_name>/', views.detalle_pokemon, name='detalle_pokemon'),
]