from django.contrib import admin
from django.urls import path, include
from .views import *

urlpatterns = [
    path('profile/', profile, name="profile"),
    path('is_authenticated/', is_authenticated, name='is_authenticated'),
]
