"""The View classes."""
from django.http import JsonResponse, HttpResponse, HttpResponseBadRequest
from drf_yasg.utils import swagger_auto_schema
from drf_yasg.openapi import Parameter, TYPE_STRING, TYPE_INTEGER, IN_QUERY
from rest_framework.views import APIView
from rest_framework.response import Response

from .factories import UserFactory, CurrencyFactory, AccountFactory, PropertyFactory
from .permissions import IsAdminOrOwner, IsAdminOrUser
from .serializers import (
    CurrencySerializer, AccountSerializer, CreatingAccountSerializer, UserSerializer, PropertySerializer,
    CreatingPropertySerializer
)
from .services.services import ServiceProtocol
from .services.user import UserServiceProtocol


class BaseView(APIView):
    """BaseView to use in concrete views."""
    _get_serializer = ...
    _post_serializer = ...
    _service: ServiceProtocol = ...

    def get(self, request, *args, **kwargs):
        filter_fields = {key: request.query_params[key] for key in request.query_params}
        instances = self._service.crud.get(**filter_fields, many=True)
        return Response(status=200, data=self._get_serializer(instances, many=True).data)

    def post(self, request, *args, **kwargs) -> HttpResponse:
        if self._post_serializer(data=request.data).is_valid():
            self._service.crud.post(**request.data)
            return HttpResponse('Done', status=201)
        else:
            return HttpResponseBadRequest('Data is not valid')

    def delete(self, request, *args, **kwargs) -> HttpResponse:
        pk = request.query_params.get('pk')
        if pk is None:
            return HttpResponseBadRequest('PK parameter is required')
        self._service.crud.delete(pk=pk)
        return HttpResponse('Done', status=201)


class CurrencyView(BaseView):
    """The view class for the Currency model."""
    _get_serializer = CurrencySerializer
    _post_serializer = CurrencySerializer
    _service: ServiceProtocol = CurrencyFactory.get_service()

    @swagger_auto_schema(request_body=CurrencySerializer)
    def post(self, request, *args, **kwargs) -> HttpResponse:
        return super().post(request, *args, **kwargs)

    @swagger_auto_schema(manual_parameters=[Parameter('pk', IN_QUERY, type=TYPE_STRING)])
    def delete(self, request, *args, **kwargs) -> HttpResponse:
        return super().delete(request, *args, **kwargs)


class AccountView(BaseView):
    """The view class for the Account model."""
    _get_serializer = AccountSerializer
    _post_serializer = CreatingAccountSerializer
    _service: ServiceProtocol = AccountFactory.get_service()
    permission_classes = [IsAdminOrOwner]

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
    permission_classes = [IsAdminOrOwner]

    @swagger_auto_schema(manual_parameters=[Parameter('id', IN_QUERY, type=TYPE_INTEGER)])
    def get(self, request, *args, **kwargs):
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
