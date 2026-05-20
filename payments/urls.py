from django.urls import path
from .views import *

urlpatterns = [
    path('', payments, name='payments'),
    path('token/', get_token, name='get_token'),
    path('webhook/izipay/', izipay_webhook, name='izipay_webhook'),
]
