from django.db import models
from .client import Client


class Transaction(models.Model):
    transaction_id = models.CharField(max_length=8, primary_key=True)
    client = models.ForeignKey(Client, on_delete=models.CASCADE, related_name="transactions")
    transaction_type = models.CharField(max_length=4, choices=[("buy", "Buy"), ("sell", "Sell")])
    transaction_date = models.DateField()
    stock_ticker = models.CharField(max_length=10)
    stock_name = models.CharField(max_length=255)
    shares = models.IntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    amount = models.DecimalField(max_digits=15, decimal_places=2)
    currency = models.CharField(max_length=3)
    transaction_status = models.CharField(max_length=50, choices=[("completed", "Completed"), ("failed", "Failed")])
    # to be generated in transformation
    transaction_channel = models.CharField(max_length=50,
                                           choices=[("online", "Online"), ("branch", "Branch"), ("ATM", "ATM")])

    class Meta:
        db_table = "transactions"
        indexes = [
            models.Index(fields=["client", "transaction_date"], name="client_date_idx"),
            models.Index(fields=["transaction_status"], name="transaction_status_idx")
        ]
        # managed = False

    def __str__(self):
        return f"{self.transaction_type} - {self.amount} {self.currency}"  # print badel l object
