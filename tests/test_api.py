from rest_framework.test import APITestCase
from rest_framework_simplejwt.tokens import RefreshToken
from api.models import Client, Transaction
from django.contrib.auth.models import User
from datetime import datetime


class TransactionAPITest(APITestCase):
    def setUp(self):
        # Create a user
        self.user = User.objects.create_user(username="testuser", password="password")

        # Generate JWT tokens for the user
        refresh = RefreshToken.for_user(self.user)
        self.access_token = str(refresh.access_token)
        self.client.credentials(HTTP_AUTHORIZATION="Bearer " + self.access_token)

        # Create a client and transactions
        self.client_obj = Client.objects.create(
            client_id="12345678",
            name="John Doe",
            email="johndoe@example.com",
            date_of_birth="1990-01-01",
            country="USA",
            account_type="premium",
            account_balance=5000.00,
            account_open_date="2020-01-01",
            status="active",
            phone_number="1234567890",
            address="123 Main St",
            risk_tolerance="medium",
            account_currency="USD",
        )
        self.transaction = Transaction.objects.create(
            transaction_id="tx123",
            client=self.client_obj,
            transaction_type="buy",
            transaction_date=datetime.now(),
            stock_ticker="AAPL",
            stock_name="Apple Inc.",
            shares=10,
            price=150.00,
            amount=1500.00,
            currency="USD",
            transaction_status="completed",
            transaction_channel="online",
        )

    def test_get_transactions_for_client(self):
        # Test fetching transactions
        response = self.client.get("/api/transactions/12345678/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['transaction_id'], "tx123")

    def test_invalid_client_id(self):
        # Test invalid client_id
        response = self.client.get("/api/transactions/invalid_id/")
        self.assertEqual(response.status_code, 404)

    def test_date_range_filter(self):
        # Test with a valid date range
        response = self.client.get("/api/transactions/12345678/?start_date=2020-01-01&end_date=2023-01-01")
        self.assertEqual(response.status_code, 200)

    def test_rate_limiting(self):
        # Exceed rate limit
        for _ in range(11):  # Exceeds 10 requests/minute limit
            self.client.get("/api/transactions/12345678/")
        response = self.client.get("/api/transactions/12345678/")
        self.assertEqual(response.status_code, 429)  # Too Many Requests
