import json
from django.shortcuts import get_object_or_404
from rest_framework import routers, status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from .models import Account
from .serializers import AccountSerializer


class AccountAPI(viewsets.ModelViewSet):
    queryset = Account.objects.all().order_by("nickname")
    serializer_class = AccountSerializer

    @action(detail=False, methods=["post"])
    def find(self, request):
        data = json.load(request)
        qs = self.queryset

        nickname = data["nickname"]

        if nickname is not None and nickname != "":
            qs = self.queryset.filter(nickname=nickname)

        page = self.paginate_queryset(qs)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(qs, many=True)
        return Response(serializer.data)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def perform_create(self, serializer):
        serializer.save()

    def retrieve(self, request, pk=None):
        account = get_object_or_404(self.queryset, pk=pk)
        serializer = self.get_serializer(account)
        return Response(serializer.data)


router = routers.DefaultRouter()
router.register(r"accounts", AccountAPI, basename="account")
