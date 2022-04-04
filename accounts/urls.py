from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from .views import (
    AccountListAPIView,
    AccountDetailAPIView,
    AccountUpdateAPIView,
    PasswordChangeAPIView,
    AccountCreateAPIView,
    AccountDeleteAPIView,
)

urlpatterns = [
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('', AccountListAPIView.as_view(), name='accounts'),
    path('create/', AccountCreateAPIView.as_view(), name='account-create'),
    path('<int:id>/', AccountDetailAPIView.as_view(), name='account-detail'),
    path('<int:id>/update/', AccountUpdateAPIView.as_view(), name='account-update'),
    path('<int:id>/delete/', AccountDeleteAPIView.as_view(), name='account-delete'),
    path('<int:id>/change-password/', PasswordChangeAPIView.as_view(), name='account-change-password'),
]
