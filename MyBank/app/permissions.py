from rest_framework import permissions


class IsAdminOrUser(permissions.BasePermission):

    def has_permission(self, request, view):
        if request.user.id and (
                request.user.is_staff or
                request.user.username == request.query_params.get('username') or
                request.user.id == request.parser_context['kwargs']['user_id']
        ):
            return True


class IsAdminOrOwner(permissions.BasePermission):

    def has_permission(self, request, view):
        if request.user.id and (request.user.is_staff or request.user.id == request.query_params.get('user_id')):
            return True
