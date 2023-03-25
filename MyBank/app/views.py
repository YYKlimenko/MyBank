from django.http import JsonResponse, HttpResponse
from drf_yasg.utils import swagger_auto_schema
from rest_framework.permissions import IsAdminUser
from rest_framework.views import APIView
from rest_framework.response import Response


from .permissions import is_admin_or_owner
from .repositories import CurrencyRepository, AccountRepository, UserRepository
from .serializers import CurrencySerializer, AccountSerializer, CreatingAccountSerializer, UserSerializer, \
    QuerySerializer


class BaseView(APIView):
    serializer = ...
    repository = ...

    def _get(self, instance, many=False):
        return self.serializer(instance, many=many).data


class CurrencyView(BaseView):
    serializer = CurrencySerializer
    repository = CurrencyRepository()

    def get(self, request, *args, **kwargs):
        filter_fields = {key: request.query_params[key] for key in request.query_params}
        currency = self.repository.get(**filter_fields, many=True)
        return Response(status=200, data=self._get(currency, True))


class AccountView(BaseView):
    serializer = AccountSerializer
    repository = AccountRepository()
    permission_classes = [IsAdminUser]

    @swagger_auto_schema(query_serializer=QuerySerializer)
    def get(self, request, *args, **kwargs):
        filter_fields = {key: request.query_params[key] for key in request.query_params}
        is_admin_or_owner(request.user, filter_fields.get('user_id'))
        queryset = self.repository.get(**filter_fields, many=True)
        return Response(status=200, data=self._get(queryset, True))

    @swagger_auto_schema(request_body=CreatingAccountSerializer)
    def post(self, request, *args, **kwargs):
        self.repository.post(request.data)
        return HttpResponse('Done')


class UserView(BaseView):
    serializer = UserSerializer
    repository = UserRepository()

    def get(self, request, *args, **kwargs):
        filter_fields = {key: request.query_params[key] for key in request.query_params}
        is_admin_or_owner(request.user, filter_fields.get('id'))
        accounts = self.repository.get(**filter_fields, many=True)
        return Response(status=200, data=self._get(accounts, True))


def count_sum(request, *args, **kwargs):
    user = UserRepository().get(id=kwargs['user_id'], prefetch_all=True)
    accounts = user.accounts.all()
    properties = user.properties.all()
    sum_ = 0

    for i in accounts:
        sum_ += i.currency.value * i.count

    for i in properties:
        sum_ += i.value

    return JsonResponse(
        {
            'user': user.username,
            'RUB': sum_,
        }
    )





