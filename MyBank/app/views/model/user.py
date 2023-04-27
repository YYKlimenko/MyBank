from django.http import JsonResponse
from drf_yasg.openapi import Parameter, IN_QUERY, TYPE_STRING
from drf_yasg.utils import swagger_auto_schema

from app.factories import UserFactory
from app.permissions import IsAdminOrUser, IsAdminOrOwner
from app.serializers import UserSerializer
from app.serializers.model import CreatingUserSerializer
from app.services import UserServiceProtocol
from app.views.base import PermitView, BaseView


class UserSumView(PermitView):
    """The view class to get sum of all accounts of a user."""
    service: UserServiceProtocol = UserFactory.get_service()
    permission_classes = {'GET': IsAdminOrUser}

    def get(self, request, *args, **kwargs):
        return JsonResponse(self.service.get_sum(user_id=kwargs['user_id']))


class UserCRUDView(BaseView):
    """The view class to make CRUD operations with the User model."""
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
