from django.contrib import admin
from django.urls import path, include
from .views import *

urlpatterns = [
    path('', products, name='products'),
    path('producto/<slug:slug>/', product_detail, name='product_detail'),
]