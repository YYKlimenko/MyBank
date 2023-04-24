from django.http import JsonResponse


from app.factories import UserFactory
from app.permissions import IsAdminOrUser
from app.services import UserServiceProtocol
from app.views.base import PermitView


class SumCounter(PermitView):
    service: UserServiceProtocol = UserFactory.get_service()
    permission_classes = {'GET': IsAdminOrUser}

    def get(self, request, *args, **kwargs):
        return JsonResponse(self.service.get_sum(user_id=kwargs['user_id']))
