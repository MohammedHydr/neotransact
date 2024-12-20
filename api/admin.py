from django.contrib import admin
from django.core.management import call_command
from django.urls import path
from django.http import HttpResponseRedirect
from django.utils.html import format_html
from django.contrib import messages

from api.models.client_transactions_summary import ClientTransactionSummary
from api.models.etl_job import ETLJob
from api.models.transaction import Transaction
from api.models.client import Client


# Register your models here.
@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    """
    Manages Client objects in the Django Admin interface.

    Features:
        - Displays key fields (e.g., client_id, name, status).
        - Allows filtering by account type and status.
        - Supports search by client ID, name, or email.
    """
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
    """
    Manages Transaction objects in the Django Admin interface.

    Features:
        - Displays key fields (e.g., transaction_id, type, status).
        - Allows filtering by type, status, and currency.
        - Supports search by transaction ID or client name.
    """

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


@admin.register(ETLJob)
class ETLJobAdmin(admin.ModelAdmin):
    """
    Manages ETL jobs in the Django Admin interface.
    Features:
        - Displays job metadata (e.g., status, start/end times).
        - Includes a button to manually trigger the ETL process.
        - Supports filtering by job status and search by name.
    """

    list_display = ("job_name", "status", "start_time", "end_time", "duration", "trigger_etl")
    list_filter = ("status",)
    search_fields = ("job_name", "error_message")
    readonly_fields = ("job_name", "status", "start_time", "end_time", "duration", "error_message")

    def trigger_etl(self, obj):
        """
        Adds a button to trigger the ETL process for monitoring purposes.
        """
        return format_html('<a class="button" href="{}">Run ETL</a>', "/admin/api/etljob/run_etl/")

    trigger_etl.short_description = "Run ETL"
    trigger_etl.allow_tags = True

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path("run_etl/", self.admin_site.admin_view(self.run_etl), name="run_etl"),
        ]
        return custom_urls + urls

    def run_etl(self, request):
        try:
            call_command("run")
            self.message_user(request, "ETL Pipeline triggered successfully.")
        except Exception as e:
            self.message_user(request, f"ETL Pipeline failed: {e}", level=messages.ERROR)
        return HttpResponseRedirect(request.META.get("HTTP_REFERER", "/admin/"))


@admin.register(ClientTransactionSummary)
class ClientTransactionSummaryAdmin(admin.ModelAdmin):
    """
    Displays summarized transaction statistics for each client for the MaterializedView.
    Features:
        - Displays total transactions, spent amount, and gained amount.
        - Supports search by client ID.
    """
    list_display = ("client_id", "total_transactions", "total_spent", "total_gained")
    search_fields = ("client_id",)
