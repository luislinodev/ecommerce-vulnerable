from django.urls import path
from .views import *

urlpatterns = [
    path("", payments, name="payments"),
    path("simulate/", simulate_payment, name="simulate_payment"),
]
