from django.urls import path
from api.views import TransactionListView

urlpatterns = [
    path('transactions/<str:client_id>/', TransactionListView.as_view(), name='transaction-list'),
]
