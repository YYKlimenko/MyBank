import logging

from django.http import HttpResponse
from drf_yasg.openapi import Parameter, TYPE_INTEGER, IN_QUERY
from drf_yasg.utils import swagger_auto_schema
from rest_framework.permissions import IsAuthenticated, IsAdminUser

from app.factories import PropertyFactory
from app.permissions import IsUser, IsRelationUser
from app.serializers import PropertySerializer, CreatingPropertySerializer
from app.serializers.model import UpdatingPropertySerializer
from app.services import ServiceProtocol
from app.views import BaseView


logger = logging.getLogger(__name__)


class PropertyView(BaseView):
    """The view class for the Property model."""
    get_serializer = PropertySerializer
    post_serializer = CreatingPropertySerializer
    service: ServiceProtocol = PropertyFactory.get_service()
    permission_classes = {
        'GET': (IsAdminUser, IsUser),
        'POST': (IsAuthenticated,),
        'PUT': (IsAdminUser, IsRelationUser),
        'DELETE': (IsAdminUser, IsRelationUser),
    }

    @swagger_auto_schema(manual_parameters=[
        Parameter('id', IN_QUERY, type=TYPE_INTEGER),
        Parameter('user_id', IN_QUERY, type=TYPE_INTEGER),
    ])
    def get(self, request, *args, **kwargs) -> HttpResponse:
        return super().get(request, *args, **kwargs)

    @swagger_auto_schema(request_body=CreatingPropertySerializer)
    def post(self, request, *args, **kwargs) -> HttpResponse:
        return super().post(request, *args, **kwargs)

    @swagger_auto_schema(
        manual_parameters=[Parameter('pk', IN_QUERY, type=TYPE_INTEGER)],
        request_body=UpdatingPropertySerializer,
    )
    def put(self, request, *args, **kwargs) -> HttpResponse:
        return super().put(request, *args, **kwargs)
