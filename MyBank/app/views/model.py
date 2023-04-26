"""The View classes."""
from django.contrib.auth.hashers import make_password
from django.http import JsonResponse, HttpResponse
from drf_yasg.utils import swagger_auto_schema
from drf_yasg.openapi import Parameter, TYPE_STRING, TYPE_INTEGER, IN_QUERY
from rest_framework.permissions import IsAuthenticated, IsAdminUser

from . import AssetBaseView, BaseView
from ..factories import UserFactory, CurrencyFactory, AccountFactory, PropertyFactory, StockFactory
from ..permissions import IsAdminOrOwner, IsAdminOrUser
from ..serializers import (
    AccountSerializer, CreatingAccountSerializer, UserSerializer, PropertySerializer, CreatingPropertySerializer
)
from ..serializers.model import CreatingUserSerializer
from ..services.base import AssetServiceProtocol, ServiceProtocol
from ..services.user import UserServiceProtocol


class CurrencyView(AssetBaseView):
    """The view class for currencies."""
    _service: AssetServiceProtocol = CurrencyFactory.get_service()
    _category_name: str = 'currency'
    permission_classes = {'POST': IsAdminUser, 'PUT': IsAdminUser, 'DELETE': IsAdminUser}


class MoexStockView(AssetBaseView):
    """The view class for moex stocks."""
    _service: AssetServiceProtocol = StockFactory.get_service()
    _category_name: str = 'moex_stock'
    permission_classes = {'POST': IsAdminUser, 'PUT': IsAdminUser, 'DELETE': IsAdminUser}


class AccountView(BaseView):
    """The view class for the Account model."""
    _get_serializer = AccountSerializer
    _post_serializer = CreatingAccountSerializer
    _service: ServiceProtocol = AccountFactory.get_service()
    permission_classes = {
        'GET': IsAdminOrOwner, 'POST': IsAuthenticated, 'PUT': IsAdminOrOwner, 'DELETE': IsAdminOrOwner
    }

    @swagger_auto_schema(manual_parameters=[Parameter('pk', IN_QUERY, type=TYPE_STRING)])
    def get(self, request, *args, **kwargs) -> HttpResponse:
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
    permission_classes = {
        'GET': IsAdminOrOwner, 'POST': IsAuthenticated, 'PUT': IsAdminOrOwner, 'DELETE': IsAdminOrOwner
    }

    @swagger_auto_schema(manual_parameters=[Parameter('id', IN_QUERY, type=TYPE_INTEGER)])
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    @swagger_auto_schema(request_body=CreatingPropertySerializer)
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)


class UserView(BaseView):
    """The view class for the User model."""
    _get_serializer = UserSerializer
    _post_serializer = CreatingUserSerializer
    _service: UserServiceProtocol = UserFactory.get_service()
    permission_classes = {
        'GET': IsAdminOrUser, 'PUT': IsAdminOrOwner, 'DELETE': IsAdminOrOwner
    }

    @swagger_auto_schema(manual_parameters=[Parameter('username', IN_QUERY, type=TYPE_STRING)])
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    @swagger_auto_schema(request_body=CreatingUserSerializer)
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)
