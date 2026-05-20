from django.contrib import admin
from django.urls import path, include
from .views import *

urlpatterns = [
    path('checkout/', checkout_view, name='checkout'),
    path('resumen/<int:order_id>/', order_summary_view, name='order_summary'),
    path('cancelar/<int:order_id>/', cancel_order_view, name='cancel_order_view'),
]
