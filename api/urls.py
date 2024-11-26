from django.urls import path
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView,
    TokenBlacklistView,
)

from api.views import TransactionView  # , DebugHeadersView

urlpatterns = [
    path("transactions/<str:client_id>/", TransactionView.as_view(), name="transaction_view"),
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('token/verify/', TokenVerifyView.as_view(), name='token_verify'),
    path('token/logout/', TokenBlacklistView.as_view(), name='token_blacklist'),
    # path("debug/", DebugHeadersView.as_view(), name="debug-headers"),
]
