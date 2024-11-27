import pandas as pd

from api.models import Transaction, Client
from etl.base import ETLBase
from etl.constants import CLIENTS_FILE, TRANSACTIONS_FILE

"""
   Extractor class responsible for extracting data from input files and preparing it for transformations.
   It extracts:
   - Client data from a CSV file.
   - Transaction data from an XLSX file while resolving references to in-memory Client objects.
"""


class Extractor(ETLBase):
    """
    Extractor class responsible for extracting data from input files and preparing it for transformations.
    It extracts:
       - Client data from a CSV file.
       - Transaction data from an XLSX file while resolving references to in-memory Client objects.
    """

    @staticmethod
    def extract_clients(clients_file=CLIENTS_FILE):
        """
        Extract client data from a CSV file and convert it into a list of Client objects.
        """
        try:
            data = pd.read_csv(clients_file)
            clients = [
                Client(**row.to_dict()) for _, row in data.iterrows()
            ]
            return clients
        except FileNotFoundError:
            raise Exception("Clients file not found: " + clients_file)
        except Exception as e:
            raise Exception("Error while extracting clients: " + str(e))

    @staticmethod
    def extract_transactions(clients, transaction_file=TRANSACTIONS_FILE):
        """
        Extract transactions and resolve client_id to in-memory Client objects.
        """
        try:
            data = pd.read_excel(transaction_file)
            transactions = []

            # Map client_id to Client object for quick lookup
            clients_dict = {client.client_id: client for client in clients}

            for _, row in data.iterrows():
                transaction_data = row.to_dict()

                # Resolve client_id to Client object from the clients_dict
                client = clients_dict.get(transaction_data["client_id"])
                if not client:
                    raise Exception(f"Client with ID {transaction_data['client_id']} does not exist.")

                # Replace the client_id in the data with the actual Client object
                transaction_data["client"] = client
                del transaction_data["client_id"]  # Remove the raw client_id

                # Create a Transaction object
                transaction = Transaction(**transaction_data)
                transactions.append(transaction)

            return transactions
        except FileNotFoundError:
            raise Exception("Transactions file not found: " + transaction_file)
        except Exception as e:
            raise Exception("Error while extracting transactions: " + str(e))
