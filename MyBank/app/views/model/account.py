from django.http import HttpResponse
from drf_yasg.openapi import Parameter, TYPE_STRING, TYPE_INTEGER, IN_QUERY
from drf_yasg.utils import swagger_auto_schema
from rest_framework.permissions import IsAuthenticated

from app.factories import AccountFactory
from app.permissions import IsAdminOrOwner
from app.serializers import AccountSerializer, CreatingAccountSerializer
from app.services import ServiceProtocol
from app.views import BaseView


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
