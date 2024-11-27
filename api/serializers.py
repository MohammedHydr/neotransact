from rest_framework import serializers
from .models import Transaction


class TransactionSerializer(serializers.ModelSerializer):
    """
        Serializes Transaction model instances into JSON format.
        Fields:
            - Includes all fields from the Transaction model.
    """
    class Meta:
        model = Transaction
        fields = '__all__'
