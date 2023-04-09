from django.http import JsonResponse, HttpResponse
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
    serializer = ...
    service: ServiceProtocol = ...

    def get(self, request, *args, **kwargs):
        filter_fields = {key: request.query_params[key] for key in request.query_params}
        instances = self.service.crud.get(**filter_fields, many=True)
        return Response(status=200, data=self.serializer(instances, many=True).data)


class CurrencyView(BaseView):
    serializer = CurrencySerializer
    service: ServiceProtocol = CurrencyFactory.get_service()


class AccountView(BaseView):
    serializer = AccountSerializer
    service: ServiceProtocol = AccountFactory.get_service()
    permission_classes = [IsAdminOrOwner]

    @swagger_auto_schema(manual_parameters=[Parameter('user_id', IN_QUERY, type=TYPE_STRING)])
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    @swagger_auto_schema(request_body=CreatingAccountSerializer)
    def post(self, request, *args, **kwargs):
        self.service.crud.post(**request.data)
        return HttpResponse('Done')

    @swagger_auto_schema(manual_parameters=[Parameter('id', IN_QUERY, type=TYPE_INTEGER)])
    def delete(self, request) -> None:
        return self.service.crud.delete(request.data['id'])


class PropertyView(BaseView):
    serializer = PropertySerializer
    service: ServiceProtocol = PropertyFactory.get_service()
    permission_classes = [IsAdminOrOwner]

    @swagger_auto_schema(manual_parameters=[Parameter('id', IN_QUERY, type=TYPE_INTEGER)])
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    @swagger_auto_schema(request_body=CreatingPropertySerializer)
    def post(self, request, *args, **kwargs):
        self.service.crud.post(**request.data)
        return HttpResponse('Done')


class UserView(BaseView):
    serializer = UserSerializer
    service: UserServiceProtocol = UserFactory.get_service()
    permission_classes = [IsAdminOrUser]


def count_sum(request, *args, **kwargs):
    service: UserServiceProtocol = UserFactory.get_service()
    return JsonResponse(service.get_sum(user_id=kwargs['user_id']))
