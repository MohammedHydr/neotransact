from etl.utils import convert_currency, log_info, log_error


class Transformer:
    """
    This class handles all transformations for clients and their transactions.

    It processes transactions for each client in chronological order, updating their balances,
    handling debt, and assigning appropriate statuses to both transactions and client accounts.
    """

    def __init__(self):
        """
        Initializes the Transformer with lists to track both successful and failed transactions.
        """
        self.failed_transactions = []
        self.successful_transactions = []

    def transform_clients_and_transactions(self, clients, transactions):
        """
        This method processes all clients and their transactions.

        Steps:
        1. Groups transactions by client.
        2. Sorts transactions for each client by transaction date.
        3. Processes transactions to update balances and statuses.

        Returns:
            - Updated clients list.
            - All transactions (successful and failed) combined into a single list.
        """
        log_info("Starting the transformation of clients and transactions.")

        # Group transactions by client
        transactions_by_client = self.group_transactions_by_client(transactions)

        # Process transactions for each client
        for client in clients:
            client_transactions = transactions_by_client.get(client.client_id, [])
            if not client_transactions:
                continue

            # Sort transactions by date
            client_transactions.sort(key=lambda t: t.transaction_date)

            # Process transactions for the client
            self.process_client_transactions(client, client_transactions)

        log_info("Transformation process completed.")
        all_transactions = self.successful_transactions + self.failed_transactions

        return clients, all_transactions

    def group_transactions_by_client(self, transactions):
        """
        Groups transactions by their client's ID.

        Args:
            transactions (list): List of Transaction objects.

        Returns:
            dict: Dictionary where the keys are client IDs and the values are lists of transactions.
        """
        grouped = {}
        for transaction in transactions:
            client_id = transaction.client.client_id
            if client_id not in grouped:
                grouped[client_id] = []
            grouped[client_id].append(transaction)
        return grouped

    def process_client_transactions(self, client, transactions):
        """
        Processes all transactions for a single client.

        If the client's account is suspended, skips all further transactions.
        """
        log_info(f"Processing transactions for client: {client.name} ({client.client_id})")

        for transaction in transactions:
            if client.status == "suspended":
                log_info(f"Skipping transactions for suspended client: {client.client_id}")
                break

            # Ensure transaction currency matches the account's currency
            if transaction.currency != client.account_currency:
                try:
                    transaction.amount = convert_currency(
                        transaction.amount, transaction.currency, client.account_currency
                    )
                    transaction.currency = client.account_currency
                except Exception as e:
                    transaction.status = "failed"
                    self.failed_transactions.append(transaction)
                    log_error(f"Currency conversion failed for transaction {transaction.transaction_id}: {e}")
                    continue

            # Process the transaction based on its type (buy or sell)
            if transaction.transaction_type == "buy":
                self.handle_buy_transaction(client, transaction)
            elif transaction.transaction_type == "sell":
                self.handle_sell_transaction(client, transaction)

    def handle_buy_transaction(self, client, transaction):
        """
        Processes a 'buy' transaction.

        - Deducts as much as possible from the balance.
        - Adds remaining amount as debt.
        - Suspends the account if the balance and debt cannot cover the transaction.

        Args:
            client (Client): The client making the purchase.
            transaction (Transaction): The buy transaction being processed.
        """
        if client.account_balance >= transaction.amount:
            # Sufficient balance; deduct and mark as successful
            client.account_balance -= transaction.amount
            transaction.status = "success"
            self.successful_transactions.append(transaction)
            log_info(f"Transaction {transaction.transaction_id} succeeded. New balance: {client.account_balance}")
        else:
            # Insufficient funds; calculate debt and suspend further buys
            remaining_amount = transaction.amount - client.account_balance
            client.debt += remaining_amount
            client.account_balance = 0  # Set balance to zero
            transaction.status = "failed"
            self.failed_transactions.append(transaction)
            log_info(f"Transaction {transaction.transaction_id} failed. Debt increased to {client.debt}.")

            # Suspend account if further transactions cannot be handled
            client.status = "suspended"
            log_info(f"Client {client.client_id} suspended due to insufficient funds.")

    def handle_sell_transaction(self, client, transaction):
        """
        Processes a 'sell' transaction.

        - Adds the transaction amount to the client's balance.
        - Reduces debt if present.
        - Reactivates the account if debt is cleared.

        Args:
            client (Client): The client making the sale.
            transaction (Transaction): The sell transaction being processed.
        """
        client.account_balance += transaction.amount

        # Reduce debt first, if applicable
        if client.debt > 0:
            if client.account_balance >= client.debt:
                client.account_balance -= client.debt
                log_info(f"Client {client.client_id} cleared debt of {client.debt}.")
                client.debt = 0
                client.status = "active"  # Reactivate account
            else:
                client.debt -= client.account_balance
                client.account_balance = 0
                log_info(f"Client {client.client_id} reduced debt to {client.debt}.")

        # Mark the transaction as successful
        transaction.status = "success"
        self.successful_transactions.append(transaction)
        log_info(f"Transaction {transaction.transaction_id} succeeded. New balance: {client.account_balance}")
