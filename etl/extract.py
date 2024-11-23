import pandas as pd
from etl.constants import CLIENTS_FILE, TRANSACTIONS_FILE


class Extractor:
    @staticmethod
    def extract_clients():
        try:
            data = pd.read_csv(CLIENTS_FILE)
            return data
        except FileNotFoundError:
            raise Exception("Clients file not found: " + CLIENTS_FILE)
        except Exception as e:
            raise Exception("Error while extracting clients: " + str(e))

    @staticmethod
    def extract_transactions():
        try:
            data = pd.read_excel(TRANSACTIONS_FILE)
            return data
        except FileNotFoundError:
            raise Exception("Transactions file not found: " + TRANSACTIONS_FILE)
        except Exception as e:
            raise Exception("Error while extracting transactions: " + str(e))
