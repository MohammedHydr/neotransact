import pandas as pd
from faker import Faker
import random
from datetime import datetime

fake = Faker()

# GET CLIENTS
clients_df = pd.read_csv("../data/clients.csv")
clients = clients_df.to_dict('records')

STOCKS = [{"ticker": "AAPL", "name": "Apple Inc."}, {"ticker": "TSLA", "name": "Tesla Inc."},
          {"ticker": "AMZN", "name": "Amazon.com Inc."}, {"ticker": "GOOGL", "name": "Alphabet Inc."},
          {"ticker": "MSFT", "name": "Microsoft Corp."}, {"ticker": "NVDA", "name": "NVIDIA Corp."}]


def generate_transactions(num_transactions):
    transactions = []
    for _ in range(num_transactions):
        client = random.choice(clients)
        client_id = client["client_id"]
        account_type = client["account_type"]

        # match amount with type
        if account_type == "standard":
            price = round(random.uniform(10, 200), 2)
            shares = random.randint(1, 50)
        elif account_type == "premium":
            price = round(random.uniform(50, 500), 2)
            shares = random.randint(1, 100)
        else:
            price = round(random.uniform(100, 1500), 2)
            shares = random.randint(10, 500)

        # account_creation_date < transaction_date < today
        account_creation_date = datetime.strptime('2023-01-01', "%Y-%m-%d").date()
        transaction_date = fake.date_between_dates(date_start=account_creation_date, date_end=datetime.today().date())

        stock = random.choice(STOCKS)
        # shares = random.randint(1, 100)
        # price = round(random.uniform(10, 1500), 2)
        transaction_id = fake.uuid4()[:8]
        transaction_type = random.choice(["buy", "sell"])
        amount = round(shares * price, 2)
        if transaction_type == "sell":
            amount = -amount  # sell => -ve
        currency = random.choice(["USD", "EUR", "GBP"])
        # transaction_status = random.choice(["completed", "pending", "failed"]) # to be set in transformation step
        transaction_channel = random.choice(["online", "branch", "ATM"])

        transactions.append({
            "transaction_id": transaction_id,
            "client_id": client_id,
            "transaction_type": transaction_type,
            "transaction_date": transaction_date,
            "stock_ticker": stock["ticker"],
            "stock_name": stock["name"],
            "shares": shares,
            "price": price,
            "amount": amount,
            "currency": currency,
            "transaction_channel": transaction_channel
        })
    return pd.DataFrame(transactions)


transactions_df = generate_transactions(3000)
transactions_df.to_excel("../data/transactions.xlsx", index=False)
