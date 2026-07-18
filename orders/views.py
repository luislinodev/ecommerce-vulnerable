from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from cart.models import Cart, CartItem
from .models import Order, OrderItem
from django.utils import timezone
from decimal import Decimal
from django.contrib import messages

# Define aquí la ubicación de tu almacén (coordenadas reales)
WAREHOUSE_LAT = -16.409047  # Ejemplo: Arequipa
WAREHOUSE_LNG = -71.537451


# Función de ejemplo para calcular transporte usando Dijkstra (por ahora fijo)
def calcular_transporte_desde_almacen(dest_lat, dest_lng):
    # Aquí deberías aplicar el algoritmo real con tus datos de rutas
    # Por ahora usamos distancia ficticia
    from math import sqrt

    distancia = sqrt((WAREHOUSE_LAT - dest_lat) ** 2 + (WAREHOUSE_LNG - dest_lng) ** 2)
    if distancia < 0.01:
        return Decimal("10.00")
    elif distancia < 0.05:
        return Decimal("20.00")
    else:
        return Decimal("30.00")


@login_required
def checkout_view(request):
    cart = get_object_or_404(Cart, user=request.user)
    cart_items = cart.items.all()

    if not cart_items.exists():
        messages.info(
            request,
            "Tu carrito está vacío. Agrega productos antes de continuar al checkout.",
        )
        return redirect("products")

    product_total = sum(item.product.price * item.quantity for item in cart_items)
    igv = round(product_total * Decimal("0.18"), 2)

    if request.method == "POST":
        event_date = request.POST.get("event_date")
        # address_text = request.POST.get('address_text')
        lat = request.POST.get("lat")
        lng = request.POST.get("lng")
        phone = request.POST.get("phone")
        comments = request.POST.get("comments", "")
        accept_terms = request.POST.get("accept_terms") == "on"

        errors = []
        if not event_date:
            errors.append("La fecha del evento es obligatoria.")
        # if not address_text:
        #     errors.append('La dirección es obligatoria.')
        if not phone:
            errors.append("El teléfono es obligatorio.")
        if not accept_terms:
            errors.append("Debes aceptar los términos y condiciones.")

        try:
            lat = float(lat)
            lng = float(lng)
        except (TypeError, ValueError):
            errors.append("Ubicación inválida.")

        if errors:
            for error in errors:
                messages.error(request, error)
            return render(
                request,
                "orders/checkout.html",
                {
                    "cart_items": cart_items,
                    "product_total": product_total,
                    "igv": igv,
                    "event_date": event_date,
                    # 'address_text': address_text,
                    "phone": phone,
                    "comments": comments,
                },
            )

        transport_cost = calcular_transporte_desde_almacen(lat, lng)
        total = round(product_total + igv + transport_cost, 2)

        order = Order.objects.create(
            user=request.user,
            event_date=event_date,
            # address_text=address_text,
            lat=lat,
            lng=lng,
            phone=phone,
            comments=comments,
            accept_terms=accept_terms,
            product_total=product_total,
            igv=igv,
            transport_cost=transport_cost,
            total=total,
            status="pendiente",
            created_at=timezone.now(),
        )

        for item in cart_items:
            OrderItem.objects.create(
                order=order,
                product=item.product,
                quantity=item.quantity,
                subtotal=item.product.price * item.quantity,
            )

        cart_items.delete()
        return redirect("order_summary", order_id=order.id)

    return render(
        request,
        "orders/checkout.html",
        {
            "cart_items": cart_items,
            "product_total": product_total,
            "igv": igv,
        },
    )


@login_required
def order_summary_view(request, order_id):
    order = get_object_or_404(Order, id=order_id, user=request.user)
    return render(request, "orders/summary.html", {"order": order})


@login_required
@require_POST
def cancel_order_view(request, order_id):
    order = get_object_or_404(Order, id=order_id, user=request.user)

    if order.status == "Pendiente":
        order.status = "Cancelado"
        order.save()
        messages.success(request, "La orden ha sido cancelada.")
    else:
        messages.warning(request, "Esta orden no puede ser cancelada.")

    return redirect("profile")  # o a donde quieras redirigir
