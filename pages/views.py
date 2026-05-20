from django.shortcuts import render
from django.contrib.auth.decorators import login_required

def home(request):
    return render(request, 'pages/home.html', {
        'show_navbar': True,
    })
    
def contacto(request):
    return render(request, 'pages/contacto.html', {
        'show_navbar': True,
    })
    
def terminos_y_condiciones(request):
    return render(request, 'pages/tyc.html', {
        'show_navbar': True,
    })