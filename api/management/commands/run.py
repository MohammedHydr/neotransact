from django.core.management.base import BaseCommand
from etl.extract import Extractor
from etl.transform import Transformer
from etl.load import Loader
from tests import test_extract, test_transform, test_load, test_utils
from etl.utils import log_info, log_error


class Command(BaseCommand):
    help = ("Run tests before the ETL pipeline. If tests pass Run the ETL process to extract, transform, "
            "and load client and transaction data.")

    def add_arguments(self, parser):
        """
        optional arguments for the command to allow targeted processing or custom behavior.
        """
        parser.add_argument(
            "--clients-only",
            action="store_true",
            help="Process only client data and skip transactions.",
        )
        parser.add_argument(
            "--transactions-only",
            action="store_true",
            help="Process only transaction data and skip clients.",
        )
        parser.add_argument(
            "--batch-size",
            type=int,
            default=1000,
            help="Specify the batch size for loading data.",
        )

    def handle(self, *args, **options):
        """
        Run tests first. If tests pass, run the ETL process.
        """
        # Step 1: Run all tests
        test_modules = [test_extract, test_transform, test_load, test_utils]
        for test_module in test_modules:
            test_module.unittest.main(exit=False)

        log_info("All tests passed. Running ETL pipeline...")

        log_info("Starting the ETL process...")

        # Initialize ETL components
        extractor = Extractor()
        transformer = Transformer()
        loader = Loader()

        # Command-line options
        process_clients = not options.get("transactions_only", False)  # Use `get` to safely access keys
        process_transactions = not options.get("clients_only", False)
        batch_size = options.get("batch_size", 1000)

        try:
            # Step 2: Extract data
            log_info("Extracting data...")
            clients = extractor.extract_clients() if process_clients else []
            transactions = extractor.extract_transactions(clients) if process_transactions else []

            # Step 3: Transform data
            log_info("Transforming data...")
            if process_clients and process_transactions:
                transformed_clients, all_transactions = transformer.transform_clients_and_transactions(clients,
                                                                                                       transactions)
            elif process_clients:
                transformed_clients, all_transactions = transformer.transform_clients_and_transactions(clients, [])
            elif process_transactions:
                transformed_clients, all_transactions = transformer.transform_clients_and_transactions([], transactions)
            else:
                transformed_clients, all_transactions = [], []

            # Step 4: Load data
            log_info("Loading data into the database...")
            if process_clients:
                loader.load_data(transformed_clients, batch_size=batch_size)
            if process_transactions:
                loader.load_data(all_transactions, batch_size=batch_size)

            log_info("ETL process completed successfully.")

        except Exception as e:
            log_error("ETL process failed: " + str(e))
            raise
