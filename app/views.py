from django.shortcuts import render
from rest_framework import routers, status, viewsets
from rest_framework.response import Response
from .models import Account
from .serializers import AccountSerializer


class AccountAPI(viewsets.ViewSet):
    queryset = Account.objects.all()
    serializer_class = AccountSerializer

    def create(self, request):
      serializer = self.get_serializer(data=request.data)
      serializer.is_valid(raise_exception=True)
      self.perform_create(serializer)
      headers = self.get_success_headers(serializer.data)
      return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def perform_create(self, serializer):
      serializer.save()


router = routers.DefaultRouter()
router.register(r"accounts", AccountAPI, basename="account")