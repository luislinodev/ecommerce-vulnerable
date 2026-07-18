from decimal import Decimal
import json
import os
import time
import requests
from uuid import UUID
from django.http import JsonResponse, HttpResponseBadRequest
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render
from orders.models import Order
from .models import Payment


def get_data_order_dynamic():
    current_time_unix = int(time.time() * 1000) * 1000  # milisegundos a microsegundos
    transaction_id = str(current_time_unix)[:14]
    order_number = str(current_time_unix)[:10]

    return {
        "currentTimeUnix": current_time_unix,
        "transactionId": transaction_id,
        "orderNumber": order_number,
    }


@csrf_exempt
def get_token(request):
    if request.method != "POST":
        return HttpResponseBadRequest("Only POST allowed")

    try:
        data = json.loads(request.body)
        # transaction_id = request.headers.get('transactionid', '')
        order_uuid = data.get("orderUUID")

        if not order_uuid:
            return JsonResponse({"error": "Falta el orderUUID"}, status=400)

        try:
            order = Order.objects.get(uuid=UUID(order_uuid))
        except Order.DoesNotExist:
            return JsonResponse({"error": "Orden no encontrada"}, status=404)

        amount = str(order.total.quantize(Decimal("0.01")))
        print(f"este es el monto total: {amount}")

        # Datos dinámicos generados desde el backend
        order_data = get_data_order_dynamic()
        transaction_id = order_data["transactionId"]
        order_number = order_data["orderNumber"]

        # Configuración segura del comercio
        MERCHANT_CODE = os.environ.get("IZIPAY_MERCHANT_CODE", "4001834")
        PUBLIC_KEY = os.environ.get("IZIPAY_PUBLIC_KEY", "")
        ORDER_CURRENCY = os.environ.get("ORDER_CURRENCY", "PEN")

        if not PUBLIC_KEY:
            return JsonResponse(
                {"error": "Izipay public key is not configured."}, status=500
            )

        payload = {
            "requestSource": "ECOMMERCE",
            "merchantCode": MERCHANT_CODE,
            "orderNumber": order_number,
            "publicKey": PUBLIC_KEY,
            "amount": amount,
            "orderCurrency": ORDER_CURRENCY,
        }

        response = requests.post(
            url=os.environ.get(
                "IZIPAY_TOKEN_URL",
                "https://sandbox-checkout.izipay.pe/apidemo/v1/Token/Generate",
            ),
            json=payload,
            headers={
                "Content-Type": "application/json",
                "transactionId": transaction_id,
            },
            timeout=15,
        )

        if response.status_code != 200:
            return JsonResponse(
                {
                    "error": "Failed to generate Izipay token",
                    "details": response.text,
                },
                status=response.status_code,
            )

        izipay_response = response.json()
        return JsonResponse(
            {
                "response": izipay_response.get("response", {}),
                "meta": {
                    "amount": amount,
                    "transactionId": transaction_id,
                    "orderNumber": order_number,
                    "merchantCode": MERCHANT_CODE,
                    "orderCurrency": ORDER_CURRENCY,
                },
            }
        )

    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)


from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from orders.models import Order
from .models import Payment


@login_required
def payments(request):

    order_uuid = request.GET.get("order_uuid")

    order = get_object_or_404(Order, uuid=order_uuid, user=request.user)

    if request.method == "POST":

        Payment.objects.create(
            transaction_id=f"SIM-{order.id}",
            order_number=str(order.id),
            amount=order.total,
            currency="PEN",
            status_code="00",
            state_message="Pago simulado",
        )

        order.status = "pagado"
        order.save()

        messages.success(request, "Pago realizado correctamente.")

        return redirect("profile")

    return render(request, "payments/index.html", {"order": order})


@csrf_exempt
def izipay_webhook(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)

            transaction_id = data.get("transactionId")
            code = data.get("code")  # status_code general

            response = data.get("response", {})
            order = response.get("order", [{}])[0]
            card = response.get("card", {})
            billing = response.get("billing", {})

            payment = Payment.objects.create(
                transaction_id=transaction_id,
                order_number=order.get("orderNumber"),
                amount=order.get("amount"),
                currency=order.get("currency"),
                status_code=code,
                state_message=order.get("stateMessage"),
                authorization_code=order.get("codeAuth"),
                date_transaction=order.get("dateTransaction"),
                time_transaction=order.get("timeTransaction"),
                unique_id=order.get("uniqueId"),
                card_brand=card.get("brand"),
                card_pan=card.get("pan"),
                first_name=billing.get("firstName"),
                last_name=billing.get("lastName"),
                email=billing.get("email"),
                phone_number=billing.get("phoneNumber"),
                document=billing.get("document"),
            )

            return JsonResponse({"status": "success", "id": payment.id})
        except Exception as e:
            return JsonResponse({"status": "error", "message": str(e)}, status=400)

    return JsonResponse({"status": "invalid request"}, status=405)


from django.shortcuts import get_object_or_404, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required

from orders.models import Order


@login_required
def simulate_payment(request):

    order_uuid = request.GET.get("order_uuid")

    order = get_object_or_404(Order, uuid=order_uuid, user=request.user)

    if order.status == "pendiente":

        order.status = "pagado"
        order.save()

        messages.success(request, "✅ Pago simulado correctamente.")

    return redirect("profile")
