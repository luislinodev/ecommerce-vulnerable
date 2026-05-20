from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from orders.models import Order

@login_required
def profile(request):
    orders = Order.objects.filter(user=request.user).order_by('-created_at')  # Obtener órdenes del usuario
    return render(request, 'account/profile.html', {
        'show_navbar': True,
        'orders': orders,
    })

def is_authenticated(request):
    return JsonResponse({'authenticated': request.user.is_authenticated})
