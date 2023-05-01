from django.http import HttpResponse, HttpResponseBadRequest
from drf_yasg.openapi import Parameter, IN_QUERY, TYPE_STRING
from drf_yasg.utils import swagger_auto_schema
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from app.serializers import AssetSerializer
from app.serializers.protocols import SerializerProtocol
from app.services import ServiceProtocol, AssetServiceProtocol


class PermitView(APIView):
    """The base view class having the upgraded permission system"""

    def get_permissions(self):
        return {key: permission() for key, permission in self.permission_classes.items()}

    def check_permissions(self, request):
        method = request.method
        permission = self.get_permissions().get(method, AllowAny())
        if not permission.has_permission(request, self):
            self.permission_denied(
                request, message=getattr(permission, 'message', None)
            )


class BaseView(PermitView):
    """BaseView to use in concrete views."""
    _get_serializer: SerializerProtocol = ...
    _post_serializer: SerializerProtocol = ...
    _service: ServiceProtocol = ...

    def get(self, request, *args, **kwargs):
        filter_fields = {key: request.query_params[key] for key in request.query_params}
        data = self._service.crud.get(**filter_fields, serializer=self._get_serializer, many=True)
        return Response(status=200, data=data)

    def post(self, request, *args, **kwargs) -> HttpResponse:
        object_ = self._post_serializer(data=request.data)
        if object_.is_valid(raise_exception=True):
            self._service.crud.post(**object_.validated_data)
            return HttpResponse('Done', status=201)
        else:
            return HttpResponseBadRequest('Data is not valid')

    def delete(self, request, *args, **kwargs) -> HttpResponse:
        pk = request.query_params.get('pk')
        if pk is None:
            return HttpResponseBadRequest('PK is required')
        self._service.crud.delete(pk=pk)
        return HttpResponse('Done', status=201)

    def put(self, request, *args, **kwargs) -> HttpResponse:
        if pk := request.query_params.get('pk'):
            self._service.crud.update(pk=pk, data=request.data)
            return HttpResponse('Done', status=201)
        else:
            return HttpResponseBadRequest('PK is required')


class AssetBaseView(BaseView):
    """BaseView to use in concrete views with TicketService."""
    _get_serializer: SerializerProtocol = AssetSerializer
    _post_serializer: SerializerProtocol = AssetSerializer
    _service: AssetServiceProtocol = ...
    _category_name: str = ...

    @swagger_auto_schema(manual_parameters=[Parameter('pk', IN_QUERY, type=TYPE_STRING)])
    def get(self, request, *args, **kwargs):
        filter_fields = {key: request.query_params[key] for key in request.query_params}
        data = self._service.crud.get(
            category_id=self._category_name, serializer=self._get_serializer, **filter_fields, many=True
        )
        return Response(status=200, data=data)

    @swagger_auto_schema(request_body=AssetSerializer)
    def post(self, request, *args, **kwargs) -> HttpResponse:
        return super().post(request, *args, **kwargs)

    @swagger_auto_schema(manual_parameters=[Parameter('pk', IN_QUERY, type=TYPE_STRING)])
    def delete(self, request, *args, **kwargs) -> HttpResponse:
        return super().delete(request, *args, **kwargs)

    @swagger_auto_schema(
        manual_parameters=[Parameter('pk', IN_QUERY, type=TYPE_STRING)], request_body=AssetSerializer
    )
    def put(self, request, *args, **kwargs) -> HttpResponse:
        pk = request.query_params.get('pk')
        if pk and self._post_serializer(data=request.data).is_valid():
            self._service.crud.update(pk=pk, data=request.data)
        else:
            self._service.updater()
        return HttpResponse('Done', status=201)
