from django.shortcuts import render

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from api.models import Transaction
from api.serializers import TransactionSerializer
from django_filters import rest_framework as filters


class TransactionFilter(filters.FilterSet):
    start_date = filters.DateTimeFilter(field_name="transaction_date", lookup_expr="gte")
    end_date = filters.DateTimeFilter(field_name="transaction_date", lookup_expr="lte")

    class Meta:
        model = Transaction
        fields = ["client", "start_date", "end_date"]


class TransactionListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, client_id):
        try:
            # Validate the client_id
            if not client_id:
                return Response({"error": "Client ID is required."}, status=status.HTTP_400_BAD_REQUEST)

            # Filter transactions by client_id and optional date range
            transactions = Transaction.objects.filter(client_id=client_id)

            start_date = request.query_params.get("start_date")
            end_date = request.query_params.get("end_date")
            if start_date:
                transactions = transactions.filter(transaction_date__gte=start_date)
            if end_date:
                transactions = transactions.filter(transaction_date__lte=end_date)

            # Serialize the data
            serializer = TransactionSerializer(transactions, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
