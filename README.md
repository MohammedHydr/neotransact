# **neotransact**

This project is a Django-based data engineering application designed to process and manage client and transaction data efficiently. It includes:
- An ETL pipeline for data ingestion and transformation.
- A RESTful API for accessing and managing transaction data.
- PostgreSQL database with partitioned tables and a materialized view for transaction summaries.
- Django Admin interface for monitoring and managing data and pipeline tasks.
- Full Dockerized setup for deployment and local development.

---

## **Table of Contents**
1. [Project Features](#project-features)
2. [Setup Instructions](#setup-instructions)
   - [Step 0: Generate CSV Files](#step-0-generate-csv-files)
   - [Step 1: Clone the Repository](#step-1-clone-the-repository)
   - [Step 2: Install Dependencies](#step-2-install-dependencies)
   - [Step 3: Configure Environment Variables](#step-3-configure-environment-variables)
   - [Step 4: Apply Migrations](#step-4-apply-migrations)
   - [Step 5: Create a Superuser](#step-5-create-a-superuser)
   - [Step 6: Start the Application](#step-6-start-the-application)
3. [Using the ETL Pipeline](#using-the-etl-pipeline)
4. [Accessing the API](#accessing-the-api)
   - [Authentication](#authentication)
   - [Endpoints](#endpoints)
5. [Running the Application with Docker](#running-the-application-with-docker)
6. [Admin Interface](#admin-interface)
7. [Testing](#testing)
8. [Project Structure](#project-structure)

---

## **Project Features**
- **ETL Pipeline**: Automates data ingestion, transformation, and loading into the PostgreSQL database.
- **Partitioned Tables**: Optimized database performance with partitioning for transaction data.
- **Materialized View**: Summarizes transaction data (total transactions, amounts spent and gained) per client.
- **Django Admin**: Manage clients, transactions, ETL jobs, and materialized views.
- **Dockerized Setup**: Streamlines development and deployment processes.
- **Testing**: Unit and integration tests for robust application logic.

---

## **Setup Instructions**

### **Step 0: Generate CSV Files**
1. Use the `Faker` library to generate mock client and transaction data.
2. Run the following command to create `clients.csv` and `transactions.xlsx` files in the `data/` directory:
   ```bash
   python scripts/generate_clients.py
   ```
   
    ```bash
   python scripts/generate_transactions.py
   ```

---

### **Step 1: Clone the Repository**
```bash
git clone <repository-url>
cd <repository-folder>
```

---

### **Step 2: Install Dependencies**
This project uses [Poetry](https://python-poetry.org/) for dependency management.

1. Install Poetry:
   ```bash
   pip install poetry
   ```

2. Install project dependencies:
   ```bash
   poetry install
   ```

3. Activate the virtual environment:
   ```bash
   poetry shell
   ```

---

### **Step 3: Configure Environment Variables**
Create a `.env` file in the project root with the following variables:
```env
DJANGO_SECRET_KEY=<your-secret-key>
DJANGO_DEBUG=True
DJANGO_ALLOWED_HOSTS=localhost,127.0.0.1
DB_NAME=<your-database-name>
DB_USER=<your-database-user>
DB_PASSWORD=<your-database-password>
DB_HOST=localhost
DB_PORT=5432
DJANGO_ADMIN_USERNAME=admin
DJANGO_ADMIN_EMAIL=admin@example.com
DJANGO_ADMIN_PASSWORD=adminpassword
```

---

### **Step 4: Apply Migrations**
Apply database migrations to create necessary tables, materialized views, and partitions:
```bash
python manage.py makemigrations
python manage.py migrate
```

---

### **Step 5: Create a Superuser**
1. Run the following command to create an admin user using environment variables:
   ```bash
   python manage.py create_admin
   ```
2. Default credentials (from `.env`):
   - **Username**: `admin`
   - **Email**: `admin@example.com`
   - **Password**: `adminpassword`

---

### **Step 6: Start the Application**
Run the development server:
```bash
python manage.py runserver
```

---

## **Using the ETL Pipeline**

### **Run the ETL Process**
Trigger the ETL process to extract, transform, and load data into the database:
```bash
python manage.py run_etl
```
Alternatively, trigger the ETL from the admin interface:
1. Log in to the admin dashboard.
2. Navigate to the **ETL Jobs** section.
3. Click "Run ETL" to start the pipeline.

---

## **Accessing the API**

### **Authentication**
1. Obtain an access token using the `/token/` endpoint:
   ```bash
   POST /token/
   {
       "username": "admin",
       "password": "adminpassword"
   }
   ```
2. Use the token in the `Authorization` header for all subsequent API requests:
   ```bash
   Authorization: Bearer <access-token>
   ```

### **Endpoints**
- **Fetch Transactions for a Client**:
  ```
  GET /transactions/<client_id>/?start_date=YYYY-MM-DD&end_date=YYYY-MM-DD
  ```
  Example:
  ```
  GET /transactions/12345/?start_date=2024-01-01&end_date=2024-01-31
  ```

---

## **Running the Application with Docker**
1. Build Docker images:
   ```bash
   docker-compose build
   ```

2. Start the application:
   ```bash
   docker-compose up
   ```

3. Access the application:
   - API: `http://localhost:8000`
   - Admin: `http://localhost:8000/admin`

---

## **Admin Interface**
1. **Login Credentials**:
   - Username: `admin`
   - Password: `adminpassword`

2. **Features**:
   - View and manage clients, transactions, ETL jobs, and materialized views.
   - Trigger the ETL pipeline from the **ETL Jobs** section.
   - View transaction summaries in the **Client Transaction Summary** section.

---

## **Testing**
Run tests to validate the ETL pipeline, API, and database logic:
```bash
python manage.py test
```

---

## **Project Structure**
## **Project Structure**
```
project/
├── api/
│   ├── management/        # Custom Django management commands
│   │   ├── commands/
│   │   │   ├── __init__.py
│   │   │   ├── create_admin.py         # Command to create a superuser from environment variables
│   │   │   ├── refresh_materialized_view.py  # Command to refresh materialized view
│   │   │   └── run.py                  # Command to run the ETL pipeline
│   ├── migrations/       # Database migrations, including partitions and materialized view setup
│   ├── models/           # Django models for clients, transactions, ETL jobs, and summaries
│   ├── admin.py          # Admin configurations for models and ETL job triggers
│   ├── serializers.py    # API serializers for data serialization
│   ├── urls.py           # API endpoint definitions
│   └── views.py          # API logic and handlers
├── config/               # Configuration files for the Django project
│   ├── __init__.py
│   ├── asgi.py
│   ├── settings.py       # Django settings with PostgreSQL, JWT, and REST configurations
│   ├── urls.py
│   └── wsgi.py
├── data/                 # Generated mock data for clients and transactions
│   ├── clients.csv
│   └── transactions.xlsx
├── etl/                  # ETL pipeline logic
│   ├── __init__.py
│   ├── base.py           # Base class for shared ETL logic
│   ├── constants.py      # Constants for file paths and configurations
│   ├── extract.py        # Extraction logic for data files
│   ├── load.py           # Data loading logic into the database
│   ├── transform.py      # Transformation logic for data processing
│   └── utils.py          # Helper functions for ETL pipeline
├── scripts/              # Scripts for generating mock data
│   ├── generate_clients.py        # Generates mock client data using Faker
│   └── generate_transactions.py  # Generates mock transaction data using Faker
├── tests/                # Unit and integration tests
│   ├── mock_data/        # Test data files
│   │   ├── clients.csv
│   │   └── transactions.xlsx
│   ├── __init__.py
│   ├── test_api.py       # API endpoint tests
│   ├── test_extract.py   # ETL extraction logic tests
│   ├── test_load.py      # ETL loading logic tests
│   ├── test_transform.py # ETL transformation logic tests
│   └── test_utils.py     # Utility function tests
├── Dockerfile            # Docker image configuration
├── docker-compose.yml    # Docker Compose configuration
├── entrypoint.sh         # Entry point script for Docker container
├── manage.py             # Django management script
├── poetry.lock           # Poetry lock file for dependencies
├── pyproject.toml        # Poetry project configuration
├── .env                  # Environment variables file
└── README.md             # Documentation for the project
```

---
## **Database Partitioning, Materialized View, and Indexing**
### **Additional Notes on Database Configuration**

- The database partitioning, materialized view, and indexing logic have been implemented using **fake migrations**. 
- These are custom SQL commands included in the migration files for better performance and database optimization.
- These migrations are not part of Django's standard model-based migrations but are written manually using `migrations.RunSQL` operations.

#### **Why Fake Migrations?**
- Partitioning and materialized views are PostgreSQL-specific features that cannot be defined directly through Django models.
- Using `migrations.RunSQL` ensures these advanced features are applied during the database setup.

#### **What to Know:**
- These fake migrations are included in the `api/migrations/` folder.
- They are automatically executed during the standard `python manage.py migrate` process.
- If you need to modify the partitioning logic or materialized view, refer to the relevant migration files.
#### **Partitioning**
- **Transactions Table**:
  - The `transactions` table is partitioned by `transaction_date` using PostgreSQL's **RANGE** partitioning.
  - Partitioning enhances performance for queries involving date-based filtering.
  - Current partitions:
    - `transactions_2024`: Covers transactions from `2024-01-01` to `2025-01-01`.
    - `transactions_2023`: Covers transactions from `2023-01-01` to `2024-01-01`.

  - SQL Commands used for partitioning:
    ```sql
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

    CREATE TABLE transactions_2024 PARTITION OF transactions
    FOR VALUES FROM ('2024-01-01') TO ('2025-01-01');

    CREATE TABLE transactions_2023 PARTITION OF transactions
    FOR VALUES FROM ('2023-01-01') TO ('2024-01-01');
    ```

#### **Materialized View**
- A **materialized view** named `client_transaction_summary` is created to aggregate transaction statistics for each client.
- Summary includes:
  - Total number of transactions.
  - Total amount spent on "buy" transactions.
  - Total amount gained from "sell" transactions.

- SQL Command for materialized view:
  ```sql
  CREATE MATERIALIZED VIEW client_transaction_summary AS
  SELECT 
      t.client_id,
      COUNT(*) AS total_transactions,
      SUM(CASE WHEN t.transaction_type = 'buy' THEN t.amount ELSE 0 END) AS total_spent,
      SUM(CASE WHEN t.transaction_type = 'sell' THEN ABS(t.amount) ELSE 0 END) AS total_gained
  FROM 
      transactions t
  GROUP BY 
      t.client_id;
  ```

- This view can be refreshed to ensure data consistency after updates using the Django management command:
  ```bash
  python manage.py refresh_materialized_view
  ```
  Alternatively, it can be refreshed via the Django Admin interface.

#### **Indexing**
- Indexes are created on both `clients` and `transactions` tables to optimize query performance:
  - **Clients Table**:
    - `account_type_idx`: Index on `account_type` for filtering by account type.
    - `country_idx`: Index on `country` for filtering by location.

  - **Transactions Table**:
    - `client_transaction_idx`: Composite index on `client_id` and `transaction_date` for faster lookups.
    - `transaction_status_idx`: Index on `transaction_status` for filtering by status.

- SQL Commands for indexing:
  ```sql
  CREATE INDEX account_type_idx ON clients (account_type);
  CREATE INDEX country_idx ON clients (country);

  CREATE INDEX client_transaction_idx ON transactions (client_id, transaction_date);
  CREATE INDEX transaction_status_idx ON transactions (transaction_status);
  ```

By using partitioning, materialized views, and indexing, this project ensures high performance and scalability for large datasets.
