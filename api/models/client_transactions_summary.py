from django.db import models


class ClientTransactionSummary(models.Model):
    client_id = models.CharField(max_length=8, primary_key=True)
    total_transactions = models.IntegerField()
    total_spent = models.DecimalField(max_digits=15, decimal_places=2)
    total_gained = models.DecimalField(max_digits=15, decimal_places=2)

    class Meta:
        managed = False
        db_table = "client_transaction_summary"
