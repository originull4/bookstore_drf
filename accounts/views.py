from core.permissions import IsAdmin, IsAdminOrOwner, IsOwner, AllowAny
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Account
from .serializers import (AccountCreateSerializer, AccountSerializer,
                          AccountUpdateSerializer, PasswordChangeSerializer)


class AccountListAPIView(APIView):
    permission_classes = [IsAdmin]

    def get(self, request):
        accounts = Account.objects.all()        
        serializer = AccountSerializer(accounts, many=True, context={'request': request})
        return Response(data=serializer.data, status=status.HTTP_200_OK)


class AccountDetailAPIView(APIView):
    permission_classes = [IsAdminOrOwner]

    def get(self, request, **kwargs):
        account = get_object_or_404(Account, id=kwargs['id'])
        self.check_object_permissions(request, account)
        serializer = AccountSerializer(account, context={'request': request})
        return Response(data=serializer.data, status=status.HTTP_200_OK)


class AccountCreateAPIView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = AccountCreateSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(data=serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class AccountUpdateAPIView(APIView):
    permission_classes = [IsAdminOrOwner]

    def put(self, request, **kwargs):
        account = get_object_or_404(Account, id=kwargs['id'])
        self.check_object_permissions(request, account)
        serializer = AccountUpdateSerializer(
            account, data=request.data, context={'request': request}, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PasswordChangeAPIView(APIView):    
    permission_classes = [IsOwner,]

    def put(self, request, **kwargs):
        account = get_object_or_404(Account, pk=kwargs['id'])
        self.check_object_permissions(request, account)
        serializer = PasswordChangeSerializer(
            instance=account, data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            msg = {"detail": "password changed successfully"}
            return Response(msg, status = status.HTTP_200_OK)        
        return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)


class AccountDeleteAPIView(APIView):
    permission_classes = [IsAdmin]

    def delete(self, request, *args, **kwargs):
        account = get_object_or_404(Account, pk=kwargs['id'])
        self.check_object_permissions(request, account)
        account.delete()

        return Response({"detail": "account deleted successfully"}, status=status.HTTP_204_NO_CONTENT)
