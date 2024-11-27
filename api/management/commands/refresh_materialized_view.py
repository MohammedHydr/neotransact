from django.core.management.base import BaseCommand
from django.db import connection


class Command(BaseCommand):
    """
        Custom Django management command to refresh the materialized view.

        Purpose:
            - Refreshes the `client_transaction_summary` materialized view in the PostgreSQL database.

        Usage:
            python manage.py refresh_materialized_view

        Notes:
            - The materialized view provides summarized transaction data (e.g., total transactions, spent, gained).
            - Run this command after updating transaction data to ensure the view remains up-to-date.
    """
    help = "Refresh the client_transaction_summary materialized view."

    def handle(self, *args, **kwargs):
        """
           Executes the SQL command to refresh the materialized view.
           Outputs a success message upon completion.
        """
        with connection.cursor() as cursor:
            cursor.execute("REFRESH MATERIALIZED VIEW client_transaction_summary;")
        self.stdout.write(self.style.SUCCESS("Materialized view refreshed successfully."))
