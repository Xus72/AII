from django.shortcuts import render, redirect
from django.db.models import Avg, Count
from django.http.response import HttpResponseRedirect, HttpResponse
from django.conf import settings
from datetime import datetime

from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required

from .utils import populate_bd
from .forms import MaridajeForm, AnyoForm
from .models import Vino,Bodega,Pais,Maridaje

# Create your views here.

def home_view(request):
    return render(request, 'main/index.html', {})

@login_required(login_url='/ingresar')
def carga_bd_view(request):

    num_obj1,num_obj2,num_obj3,num_obj4 = populate_bd()
    logout(request)
    mensaje = (
        "Se han registrado " 
        + str(num_obj1) + " bodegas, " 
        + str(num_obj2) + " países, "
        + str(num_obj3) + " maridajes y "
        + str(num_obj2) + " Vinos."
    )

    context = {
        'mensaje':mensaje,
    }
    return render(request, 'main/carga.html', context)

def ingreso_view(request):

    if request.user.is_authenticated:
        return(HttpResponseRedirect('/carga'))
    formulario = AuthenticationForm()
    if request.method=='POST':
        formulario = AuthenticationForm(request.POST)
        usuario=request.POST['username']
        clave=request.POST['password']
        acceso=authenticate(username=usuario,password=clave)
        if acceso is not None:
            if acceso.is_active:
                login(request, acceso)
                return (HttpResponseRedirect('/carga'))
            else:
                return (HttpResponse('<html><body>ERROR: USUARIO NO ACTIVO </body></html>'))
        else:
            return (HttpResponse('<html><body>ERROR: USUARIO O CONTRASE&Ntilde;A INCORRECTOS </body></html>'))
                     
    return render(request, 'main/ingresar.html', {'formulario':formulario})

def busqueda_maridaje_view(request):
    formulario = MaridajeForm()
    busqueda = None
    maridaje = None
    nombre_maridaje = None
    if request.method == 'POST':
        maridaje =  request.POST.get('busqueda')
        if maridaje:
            busqueda = Vino.objects.filter(maridaje=maridaje)
            nombre_maridaje = Maridaje.objects.get(idMaridaje=maridaje)
    context = {
        'formulario':formulario,
        'busqueda':busqueda,
        'nombre_maridaje':nombre_maridaje,
    }
    return render(request, 'main/vinos_maridaje.html', context)

def vinos_pais(request):

    paises = Pais.objects.all()
    lista_vinos_pais = list()
    
    for i in range(len(paises)):
      lista_vinos_pais.append((paises[i],Vino.objects.filter(pais=i)))

    context = {
        'lista_vinos_pais': lista_vinos_pais,
    }
    return render(request, 'main/vinos_pais.html', context)

def vinos_anyo(request):
    formulario = AnyoForm()
    busqueda = None
    anyo = None

    if request.method == 'POST':
        formulario = AnyoForm(request.POST)
        if formulario.is_valid():
            busqueda = Vino.objects.filter(anyo__lte = formulario.cleaned_data['busqueda'])
            anyo = formulario.cleaned_data['busqueda']
    context = {
        'formulario':formulario,
        'busqueda':busqueda,
        'anyo':anyo
    }

    return render(request, 'main/vinos_anyo.html', context)

def logout_view(request):
    logout(request)
    return redirect('/')