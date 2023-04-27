from drf_yasg.openapi import Parameter, TYPE_INTEGER, IN_QUERY
from drf_yasg.utils import swagger_auto_schema
from rest_framework.permissions import IsAuthenticated

from app.factories import PropertyFactory
from app.permissions import IsAdminOrOwner
from app.serializers import PropertySerializer, CreatingPropertySerializer
from app.services import ServiceProtocol
from app.views import BaseView


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
