# Generated by Django 5.1.3 on 2024-11-24 20:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Transaction',
            fields=[
                ('transaction_id', models.CharField(max_length=8, primary_key=True, serialize=False)),
                ('transaction_type', models.CharField(choices=[('buy', 'Buy'), ('sell', 'Sell')], max_length=4)),
                ('transaction_date', models.DateTimeField()),
                ('stock_ticker', models.CharField(max_length=10)),
                ('stock_name', models.CharField(max_length=255)),
                ('shares', models.IntegerField()),
                ('price', models.DecimalField(decimal_places=2, max_digits=10)),
                ('amount', models.DecimalField(decimal_places=2, max_digits=15)),
                ('currency', models.CharField(max_length=3)),
                ('transaction_status', models.CharField(choices=[('completed', 'Completed'), ('failed', 'Failed')], max_length=50)),
                ('transaction_channel', models.CharField(choices=[('online', 'Online'), ('branch', 'Branch'), ('ATM', 'ATM')], max_length=50)),
            ],
            options={
                'db_table': 'transactions',
                'managed': False,
            },
        ),
    ]
