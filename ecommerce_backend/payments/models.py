from django.db import models


class Transaction(models.Model):
    user_email = models.EmailField()
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_method = models.CharField(max_length=50)  # 'stripe' or 'paystack'
    transaction_id = models.CharField(max_length=100, unique=True)
    status = models.CharField(max_length=20)  # 'success', 'failed'
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.payment_method} - {self.transaction_id}"
