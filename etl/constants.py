import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(BASE_DIR, 'data')

CLIENTS_FILE = os.path.join(DATA_DIR, 'clients.csv')
TRANSACTIONS_FILE = os.path.join(DATA_DIR, 'transactions.xlsx')
