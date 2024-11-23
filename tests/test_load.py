import unittest
from datetime import date
from api.models.client import Client
from etl.load import Loader


class TestLoader(unittest.TestCase):
    def setUp(self):
        self.clients = [
            Client(
                client_id="1",
                name="Lorem Ipsum",
                email="lorem.ipsum@example.com",
                date_of_birth=date(1980, 5, 15),
                country="LEBANON",
                account_type="standard",
                account_balance=1700,
                account_open_date=date(2000, 6, 1),
                status="active",
                phone_number="123-456-7890",
                address="123 Main St, BEIRUT",
                risk_tolerance="low",
                account_currency="USD",
                debt=0.00,
            ),
            Client(
                client_id="2",
                name="Moe Haydar",
                email="moe.haydar@example.com",
                date_of_birth=date(1990, 10, 22),
                country="LEBANON",
                account_type="premium",
                account_balance=-1000,
                account_open_date=date(2010, 8, 15),
                status="suspended",
                phone_number="321-654-0987",
                address="456 Side St, BEIRUT",
                risk_tolerance="medium",
                account_currency="USD",
                debt=1000.00,
            ),
        ]

    def test_load_clients(self):
        """
        Test that clients are loaded into the database successfully.
        """
        loader = Loader()
        loader.load_data(self.clients)

        # Check that clients are saved in the database
        self.assertEqual(Client.objects.count(), 2)
        client_1 = Client.objects.get(client_id="1")
        client_2 = Client.objects.get(client_id="2")

        # Verify data for the first client
        self.assertEqual(client_1.name, "Lorem Ipsum")
        self.assertEqual(client_1.account_balance, 1700)

        # Verify data for the second client
        self.assertEqual(client_2.name, "Moe Haydar")
        self.assertEqual(client_2.status, "suspended")
        self.assertEqual(client_2.debt, 1000.00)


if __name__ == "__main__":
    unittest.main()
