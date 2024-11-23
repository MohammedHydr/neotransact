from django.db import transaction


class Loader:
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
                for i in range(0, len(model_instances), batch_size):
                    batch = model_instances[i:i + batch_size]
                    if batch:
                        batch[0].__class__.objects.bulk_create(batch, batch_size=batch_size)
                print("SAVED " + str(len(model_instances)) + " records.")
        except Exception as e:
            raise Exception("Error loading data: " + str(e))
