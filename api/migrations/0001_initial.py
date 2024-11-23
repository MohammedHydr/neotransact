from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        # Create the 'clients' table
        migrations.CreateModel(
            name='Client',
            fields=[
                ('client_id', models.CharField(max_length=8, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=255)),
                ('email', models.EmailField(max_length=254, unique=True)),
                ('date_of_birth', models.DateField()),
                ('country', models.CharField(max_length=100)),
                ('account_type', models.CharField(choices=[('standard', 'Standard'), ('premium', 'Premium'), ('corporate', 'Corporate')], max_length=50)),
                ('account_balance', models.DecimalField(decimal_places=2, max_digits=15)),
                ('account_open_date', models.DateField()),
                ('status', models.CharField(choices=[('active', 'Active'), ('Suspended', 'suspended')], max_length=50)),
                ('phone_number', models.CharField(max_length=50)),
                ('address', models.TextField()),
                ('risk_tolerance', models.CharField(choices=[('low', 'Low'), ('medium', 'Medium'), ('high', 'High')], max_length=50)),
                ('account_currency', models.CharField(max_length=3)),
                ('debt', models.DecimalField(decimal_places=2, default=0.0, max_digits=15)),
            ],
            options={
                'db_table': 'clients',
                'indexes': [
                    models.Index(fields=['account_type'], name='account_type_id_idx'),
                    models.Index(fields=['country'], name='country_idx'),
                ],
            },
        ),

        # Create the 'transactions' table with partitioning logic
        migrations.RunSQL(
            """
            CREATE TABLE transactions (
                transaction_id VARCHAR(8) NOT NULL,
                transaction_date DATE NOT NULL,
                client_id VARCHAR(8) NOT NULL,
                transaction_type VARCHAR(4) NOT NULL,
                stock_ticker VARCHAR(10),
                stock_name VARCHAR(255),
                shares INTEGER,
                price NUMERIC(10, 2),
                amount NUMERIC(15, 2),
                currency VARCHAR(3),
                transaction_status VARCHAR(50),
                transaction_channel VARCHAR(50),
                PRIMARY KEY (transaction_id, transaction_date),  -- Primary key includes partition key
                FOREIGN KEY (client_id) REFERENCES clients (client_id)
            ) PARTITION BY RANGE (transaction_date);
            """,
            reverse_sql="DROP TABLE transactions;",
        ),

        # Create partitions for the 'transactions' table
        migrations.RunSQL(
            """
            CREATE TABLE transactions_2024 PARTITION OF transactions
            FOR VALUES FROM ('2024-01-01') TO ('2025-01-01');
            """,
            reverse_sql="DROP TABLE transactions_2024;",
        ),
        migrations.RunSQL(
            """
            CREATE TABLE transactions_2023 PARTITION OF transactions
            FOR VALUES FROM ('2023-01-01') TO ('2024-01-01');
            """,
            reverse_sql="DROP TABLE transactions_2023;",
        ),

        # Create indexes for optimized queries on the 'transactions' table
        migrations.RunSQL(
            """
            CREATE INDEX client_transaction_idx ON transactions (client_id, transaction_date);
            CREATE INDEX transaction_status_idx ON transactions (transaction_status);
            """,
            reverse_sql="""
            DROP INDEX IF EXISTS client_transaction_idx;
            DROP INDEX IF EXISTS transaction_status_idx;
            """,
        ),
    ]
