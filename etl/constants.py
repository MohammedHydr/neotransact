import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(BASE_DIR, 'data')

CLIENTS_FILE = os.path.join(DATA_DIR, 'clients.csv')
TRANSACTIONS_FILE = os.path.join(DATA_DIR, 'transactions.xlsx')


FIXED_CURRENCY_RATES = {
    ("EUR", "USD"): 1.10,  # 1 EUR = 1.10 USD
    ("GBP", "USD"): 1.25,
    ("USD", "EUR"): 0.91,
    ("USD", "GBP"): 0.80,
}