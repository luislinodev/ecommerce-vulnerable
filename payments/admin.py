from django.contrib import admin
from .models import Payment

@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ('transaction_id', 'amount', 'currency', 'email', 'status_code', 'created_at')
    search_fields = ('transaction_id', 'email', 'order_number')
