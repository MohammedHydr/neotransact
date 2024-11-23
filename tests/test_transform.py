import unittest
from api.models.client import Client
from api.models.transaction import Transaction
from etl.transform import Transformer


class TestTransformer(unittest.TestCase):
    def setUp(self):
        """
        Set up mock clients and transactions.
        """
        self.clients = [
            Client(client_id="1", name="Lorem Ipsum", account_balance=1500, debt=0, status="active", account_currency="USD"),
            Client(client_id="2", name="Moe Haydar", account_balance=2000, debt=0, status="active", account_currency="USD"),
        ]
        self.transactions = [
            Transaction(transaction_id="txn001", client=self.clients[0], transaction_type="buy", transaction_date="2024-01-01", amount=500, currency="USD"),
            Transaction(transaction_id="txn002", client=self.clients[0], transaction_type="sell", transaction_date="2024-01-02", amount=700, currency="USD"),
            Transaction(transaction_id="txn003", client=self.clients[1], transaction_type="buy", transaction_date="2024-01-01", amount=3000, currency="USD"),
        ]

    def test_transform_clients_and_transactions(self):
        """
        Test transformation logic for clients and transactions.
        """
        transformer = Transformer()
        transformed_clients, all_transactions = transformer.transform_clients_and_transactions(self.clients, self.transactions)

        # Check client balances and statuses
        self.assertEqual(transformed_clients[0].account_balance, 1700)  # 1500 - 500 + 700
        self.assertEqual(transformed_clients[1].account_balance, 0)     # Moe Haydar has insufficient funds
        self.assertEqual(transformed_clients[1].debt, 1000)            # Moe Haydar owes 1000
        self.assertEqual(transformed_clients[1].status, "suspended")   # Account suspended

        # Check transaction statuses
        self.assertEqual(all_transactions[0].status, "success")
        self.assertEqual(all_transactions[2].status, "failed")


if __name__ == "__main__":
    unittest.main()
