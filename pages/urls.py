from django.contrib import admin
from django.urls import path, include
from .views import *

urlpatterns = [
    path('', home, name='home'),
    path('contacto/', contacto, name='contacto'),
    path('tyc/', terminos_y_condiciones, name='terminos_y_condiciones'),
]
