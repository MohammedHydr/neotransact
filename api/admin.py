from django.contrib import admin

from .models.transaction import Transaction
from .models.client import Client


# Register your models here.

@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = (
        "client_id",
        "name",
        "email",
        "account_type",
        "account_balance",
        "debt",
        "status",
    )
    search_fields = ("client_id", "name", "email")
    list_filter = ("account_type", "status")


@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = (
        "transaction_id",
        "client",
        "transaction_type",
        "transaction_date",
        "amount",
        "transaction_status",
    )
    search_fields = ("transaction_id", "client__name")
    list_filter = ("transaction_type", "transaction_status", "currency")
