import unittest
import os
from etl.extract import Extractor


class TestExtractor(unittest.TestCase):
    def setUp(self):
        self.mock_clients_path = os.path.join(os.path.dirname(__file__), "mock_data", "clients.csv")
        self.mock_transactions_path = os.path.join(os.path.dirname(__file__), "mock_data", "transactions.xlsx")

    def test_extract_clients(self):
        extractor = Extractor()
        clients = extractor.extract_clients(self.mock_clients_path)
        self.assertEqual(len(clients), 2)
        self.assertEqual(clients[0].name, "Lorem Ipsum")
        self.assertEqual(clients[1].name, "Moe Haydar")

    def test_extract_transactions(self):
        """
        Test extracting transactions from the mock Excel file.
        """
        extractor = Extractor()
        transactions = extractor.extract_transactions(self.mock_transactions_path)
        self.assertEqual(len(transactions), 3)
        self.assertEqual(transactions[0].transaction_id, "txn001")
        self.assertEqual(transactions[2].amount, 2000)


if __name__ == "__main__":
    unittest.main()
