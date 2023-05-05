from rest_framework import permissions


class IsUser(permissions.BasePermission):

    def has_permission(self, request, view):
        if request.user.id and (
                request.user.username == request.query_params.get('username') or
                request.user.id == request.query_params.get('user_id')
        ):
            return True


class IsRelationUser(permissions.BasePermission):

    def has_permission(self, request, view):
        if request.user.id:
            instance = view.service.crud.get(
                pk=request.query_params.get('pk'),
                serializer=view.get_serializer,
            )
            return request.user.id == instance['user_id']
