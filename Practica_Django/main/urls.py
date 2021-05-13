from django.urls import path
from .views import (
    home_view,
    carga_bd_view,
    vinos_pais,
    busqueda_maridaje_view,
    ingreso_view,
    vinos_anyo
)

app_name = 'main'
urlpatterns = [
    path('',home_view),
    path('carga/', carga_bd_view),
    #path('carga/', views.carga_bd_view),
    path('ingresar/', ingreso_view, name="ingresar"),
    path('vinos_maridaje/', busqueda_maridaje_view),
    path('vinos_pais/', vinos_pais),
    path('vinos_anyo/', vinos_anyo),
]