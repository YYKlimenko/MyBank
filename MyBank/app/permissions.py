from django.http import HttpResponseForbidden


def is_admin_or_owner(current_user, owner_id):
    if current_user.is_staff or current_user.id == owner_id:
        return True
    else:
        return HttpResponseForbidden()
