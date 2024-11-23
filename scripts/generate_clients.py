import pandas as pd
from faker import Faker
import random
from datetime import timedelta

# Lebanese DATA
fake = Faker()

"""
The `Faker` library is a Python package used to generate synthetic data for testing and prototyping. 
In this context, we use `Faker` to create realistic client information, such as names, emails, dates of 
birth, phone numbers, and addresses. This is particularly useful when no real data is available, as it 
allows us to simulate a production-like dataset without violating privacy concerns.

Additionally, we enhance realism by pairing `Faker` with Python’s `random` module to assign 
attributes such as account types, risk tolerances, and account balances based on weighted 
probabilities, ensuring more realistic and diverse synthetic data.
"""


def generate_clients(num_clients):
    clients = []
    for _ in range(num_clients):
        # make wieghts realistic
        account_type = random.choices(["standard", "premium", "corporate"], weights=[60, 30, 10], k=1)[0]
        # match type with balance also for more realistic
        account_balance = {
            "standard": round(random.uniform(1000, 50000), 2),
            "premium": round(random.uniform(50001, 200000), 2),
            "corporate": round(random.uniform(200001, 1000000), 2)}[account_type]
        risk_tolerance = {
            "standard": "low",
            "premium": "medium",
            "corporate": "high"}[account_type]
        client_id = fake.uuid4()[:8]
        name = fake.name()
        email = fake.email()
        date_of_birth = fake.date_of_birth(minimum_age=18, maximum_age=80)
        account_open_date = fake.date_between(start_date=date_of_birth + timedelta(days=6570))  # >dob
        country = fake.country()
        # status = random.choices(["active", "inactive", "suspended"], weights=[85, 10, 5], k=1)[0]
        phone_number = fake.phone_number()
        address = fake.address()
        # risk_tolerance = random.choice(["low", "medium", "high"])
        account_currency = random.choice(["USD", "EUR", "GBP"])

        clients.append({
            "client_id": client_id,
            "name": name,
            "email": email,
            "date_of_birth": date_of_birth,
            "country": country,
            "account_type": account_type,
            "account_balance": account_balance,
            "account_open_date": account_open_date,
            "phone_number": phone_number,
            "address": address,
            "risk_tolerance": risk_tolerance,
            "account_currency": account_currency
        })
    return pd.DataFrame(clients)


clients_df = generate_clients(100)
clients_df.to_csv("../data/clients.csv", index=False)
