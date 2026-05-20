from django.db import models

class Payment(models.Model):
    transaction_id = models.CharField(max_length=100)
    order_number = models.CharField(max_length=100)
    amount = models.CharField(max_length=20)
    currency = models.CharField(max_length=10)
    status_code = models.CharField(max_length=10)
    state_message = models.CharField(max_length=100)
    authorization_code = models.CharField(max_length=20)
    date_transaction = models.CharField(max_length=20)
    time_transaction = models.CharField(max_length=20)
    unique_id = models.CharField(max_length=100)
    card_brand = models.CharField(max_length=10)
    card_pan = models.CharField(max_length=25)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField()
    phone_number = models.CharField(max_length=20)
    document = models.CharField(max_length=20)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Pago {self.order_number} - {self.transaction_id}"
