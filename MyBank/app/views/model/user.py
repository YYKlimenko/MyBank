from django.http import JsonResponse, HttpResponse
from drf_yasg.openapi import Parameter, IN_QUERY, TYPE_STRING, TYPE_INTEGER
from drf_yasg.utils import swagger_auto_schema
from rest_framework.permissions import IsAdminUser

from app.factories import UserFactory
from app.permissions import IsUser
from app.serializers import UserSerializer
from app.serializers.model import CreatingUserSerializer
from app.serializers.protocols import SerializerProtocol
from app.services import UserServiceProtocol
from app.views.base import PermitView, BaseView


class UserSumView(PermitView):
    """The view class to get sum of all accounts of a user."""
    service: UserServiceProtocol = UserFactory.get_service()
    permission_classes = {'GET': (IsAdminUser, IsUser)}

    @swagger_auto_schema(manual_parameters=[Parameter('user_id', IN_QUERY, type=TYPE_INTEGER, required=True)])
    def get(self, request, *args, **kwargs):
        return JsonResponse(self.service.counter.get_sum(user_id=request.query_params.get('user_id')))


class UserCRUDView(BaseView):
    """The view class to make CRUD operations with the User model."""
    get_serializer: SerializerProtocol = UserSerializer
    post_serializer: SerializerProtocol = CreatingUserSerializer
    service: UserServiceProtocol = UserFactory.get_service()
    permission_classes = {
        'GET': (IsAdminUser, IsUser), 'PUT': (IsAdminUser, IsUser), 'DELETE': (IsAdminUser, IsUser)
    }

    @swagger_auto_schema(manual_parameters=[Parameter('username', IN_QUERY, type=TYPE_STRING)])
    def get(self, request, *args, **kwargs) -> HttpResponse:
        return super().get(request, *args, **kwargs)

    @swagger_auto_schema(request_body=CreatingUserSerializer)
    def post(self, request, *args, **kwargs) -> HttpResponse:
        return super().post(request, *args, **kwargs)

    @swagger_auto_schema(manual_parameters=[Parameter('pk', IN_QUERY, type=TYPE_INTEGER)])
    def delete(self, request, *args, **kwargs) -> HttpResponse:
        return super().delete(request, *args, **kwargs)

    @swagger_auto_schema(manual_parameters=[
        Parameter('pk', IN_QUERY, type=TYPE_INTEGER),
    ],
        request_body=CreatingUserSerializer)
    def put(self, request, *args, **kwargs) -> HttpResponse:
        return super().put(request, *args, **kwargs)
