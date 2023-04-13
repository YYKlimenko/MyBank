from django.http import JsonResponse

from app.factories import UserFactory
from app.services import UserServiceProtocol


def count_sum(request, *args, **kwargs):
    service: UserServiceProtocol = UserFactory.get_service()
    return JsonResponse(service.get_sum(user_id=kwargs['user_id']))
