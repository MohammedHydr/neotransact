from datetime import datetime

from django.core.exceptions import ValidationError
from django.utils.decorators import method_decorator
from django_ratelimit.decorators import ratelimit
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.throttling import UserRateThrottle
from rest_framework_simplejwt.authentication import JWTAuthentication
from django.http import JsonResponse

from api.models import Transaction, Client

from api.serializers import TransactionSerializer


@method_decorator(ratelimit(key='ip', rate='5/m', block=True), name='dispatch')
@method_decorator(ratelimit(key='ip', rate='100/h', block=True), name='dispatch')
@method_decorator(ratelimit(key='user', rate='10/m', block=True), name='dispatch')
class TransactionView(APIView):
    """
    Handles API requests to fetch transactions for a specific client.
    Features:
        - Fetches transactions by client ID.
        - Supports optional date range filtering (start_date, end_date).
        - Implements rate-limiting to prevent abuse.
        - Secures the endpoint with JWT authentication.
    """
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    throttle_classes = [UserRateThrottle]

    def get(self, request, client_id):
        try:
            # Look for the client by ID
            client = Client.objects.get(client_id=client_id.strip())

            # Optional date range filtering
            start_date = request.query_params.get('start_date')
            end_date = request.query_params.get('end_date')

            # Validate and parse dates
            if start_date:
                start_date = datetime.strptime(start_date, "%Y-%m-%d")
            if end_date:
                end_date = datetime.strptime(end_date, "%Y-%m-%d")
                if start_date and start_date > end_date:
                    raise ValidationError("start_date cannot be after end_date")

            # Filter transactions for the client
            transactions = Transaction.objects.filter(client=client)
            if start_date:
                transactions = transactions.filter(transaction_date__gte=start_date)
            if end_date:
                transactions = transactions.filter(transaction_date__lte=end_date)

            # Serialize and return transactions
            serializer = TransactionSerializer(transactions, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)

        except Client.DoesNotExist:
            return Response({"error": "Client not found"}, status=status.HTTP_404_NOT_FOUND)
        except ValueError:
            return Response({"error": "Invalid date format. Use YYYY-MM-DD"}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({"error": "Something went wrong: " + str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


def rate_limit_exceeded_view(request, exception=None):
    return JsonResponse({"error": "Rate limit exceeded. Please try again later."}, status=429)

# class DebugHeadersView(APIView):
#     permission_classes = [IsAuthenticated]
#
#     def get(self, request):
#         print(request.headers)
#         return Response({"message": "Headers received"})
