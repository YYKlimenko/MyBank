"""The View classes."""
from django.http import JsonResponse, HttpResponse
from drf_yasg.utils import swagger_auto_schema
from drf_yasg.openapi import Parameter, TYPE_STRING, TYPE_INTEGER, IN_QUERY
from rest_framework.permissions import IsAuthenticated

from . import AssetBaseView, BaseView
from ..factories import UserFactory, CurrencyFactory, AccountFactory, PropertyFactory, StockFactory
from ..permissions import IsAdminOrOwner, IsAdminOrUser
from ..serializers import (
    AccountSerializer, CreatingAccountSerializer, UserSerializer, PropertySerializer, CreatingPropertySerializer
)
from ..services.base import AssetServiceProtocol, ServiceProtocol
from ..services.user import UserServiceProtocol

from rest_framework.permissions import IsAdminUser


class CurrencyView(AssetBaseView):
    """The view class for currencies."""
    _service: AssetServiceProtocol = CurrencyFactory.get_service()
    _category_name: str = 'currency'


class MoexStockView(AssetBaseView):
    """The view class for moex stocks."""
    _service: AssetServiceProtocol = StockFactory.get_service()
    _category_name: str = 'moex_stock'


class AccountView(BaseView):
    """The view class for the Account model."""
    _get_serializer = AccountSerializer
    _post_serializer = CreatingAccountSerializer
    _service: ServiceProtocol = AccountFactory.get_service()
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(manual_parameters=[Parameter('pk', IN_QUERY, type=TYPE_STRING)])
    def get(self, request, *args, **kwargs) -> HttpResponse:
        print(request.user)
        return super().get(request, *args, **kwargs)

    @swagger_auto_schema(request_body=CreatingAccountSerializer)
    def post(self, request, *args, **kwargs) -> HttpResponse:
        return super().post(request, *args, **kwargs)

    @swagger_auto_schema(manual_parameters=[Parameter('pk', IN_QUERY, type=TYPE_INTEGER)])
    def delete(self, request, *args, **kwargs) -> HttpResponse:
        return super().delete(request, *args, **kwargs)


class PropertyView(BaseView):
    """The view class for the Property model."""
    _get_serializer = PropertySerializer
    _post_serializer = CreatingPropertySerializer
    _service: ServiceProtocol = PropertyFactory.get_service()
    permission_classes = [IsAdminOrOwner]

    @swagger_auto_schema(manual_parameters=[Parameter('id', IN_QUERY, type=TYPE_INTEGER)])
    def get(self, request, *args, **kwargs):
        print(request.user)
        return super().get(request, *args, **kwargs)

    @swagger_auto_schema(request_body=CreatingPropertySerializer)
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)


class UserView(BaseView):
    """The view class for the User model."""
    _get_serializer = UserSerializer
    _service: UserServiceProtocol = UserFactory.get_service()
    permission_classes = [IsAdminOrUser]


def count_sum(request, *args, **kwargs):
    service: UserServiceProtocol = UserFactory.get_service()
    return JsonResponse(service.get_sum(user_id=kwargs['user_id']))
