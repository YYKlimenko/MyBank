from django.http import JsonResponse
from rest_framework.decorators import api_view
from rest_framework.views import APIView

from app.factories import UserFactory
from app.permissions import IsAdminOrUser
from app.services import UserServiceProtocol


class SumCounter(APIView):
    service: UserServiceProtocol = UserFactory.get_service()
    permission_classes = [IsAdminOrUser]

    def get(self, request, *args, **kwargs):
        return JsonResponse(self.service.get_sum(user_id=kwargs['user_id']))
