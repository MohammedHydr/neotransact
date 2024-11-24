from django.core.management.base import BaseCommand
from django.db import connection


class Command(BaseCommand):
    help = "Refresh the client_transaction_summary materialized view."

    def handle(self, *args, **kwargs):
        with connection.cursor() as cursor:
            cursor.execute("REFRESH MATERIALIZED VIEW client_transaction_summary;")
        self.stdout.write(self.style.SUCCESS("Materialized view refreshed successfully."))
