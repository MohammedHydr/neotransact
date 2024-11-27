from django.core.management import call_command
from django.db import transaction


class Loader:
    """
    Loader class to handle saving data into the PostgreSQL database in an efficient manner.

    Includes:
    - Bulk inserts for scalability.
    - Materialized view refresh after data loading.
    - Trunkate table to show the process when run
    """

    @staticmethod
    def load_data(model_instances, batch_size=1000):
        """
        Save data into the database using bulk_create for efficiency Not suitable
        for my case small sample but for scalability
        """
        try:
            model_class = model_instances[0].__class__  # Get the model class (eza client aw transaction)
            with transaction.atomic():
                model_class.objects.all().delete()  # TODO: REMOVE TRUNCATE
                # Split data into batches and save using bulk_create
                for i in range(0, len(model_instances), batch_size):  # Batch insertion for efficiency
                    batch = model_instances[i:i + batch_size]
                    if batch:
                        batch[0].__class__.objects.bulk_create(batch, batch_size=batch_size)
                print("SAVED " + str(len(model_instances)) + " records.")
                call_command("refresh_materialized_view")
                print("Materialized view refreshed after batch load.")
        except Exception as e:
            raise Exception("Error loading data: " + str(e))
