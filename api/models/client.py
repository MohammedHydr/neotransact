from django.db import models
from django.contrib.auth.models import User


class Client(models.Model):
    client_id = models.CharField(max_length=8, primary_key=True)  # Use the generated UUID
    name = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    date_of_birth = models.DateField()
    country = models.CharField(max_length=100)
    account_type = models.CharField(max_length=50, choices=[("standard", "Standard"), ("premium", "Premium"),
                                                            ("corporate", "Corporate")])
    account_balance = models.DecimalField(max_digits=15, decimal_places=2)
    account_open_date = models.DateField()
    status = models.CharField(max_length=50, choices=[("active", "Active"), ("Suspended", "suspended")])
    phone_number = models.CharField(max_length=50)
    address = models.TextField()
    risk_tolerance = models.CharField(max_length=50, choices=[("low", "Low"), ("medium", "Medium"), ("high", "High")])
    account_currency = models.CharField(max_length=3)
    debt = models.DecimalField(max_digits=15, decimal_places=2, default=0.00)  # to be generated in transformation

    class Meta:  # postgres tb name
        db_table = "clients"
        indexes = [
            models.Index(fields=["account_type"], name="account_type_id_idx"),
            models.Index(fields=["country"], name="country_idx"),
        ]

    def __str__(self):
        return self.name
