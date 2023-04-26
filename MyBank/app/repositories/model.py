from django.contrib.auth import get_user_model

from app.models.protocols import UserModelProtocol
from app.repositories import CRUDHandler


class UserCrudHandler(CRUDHandler):
    model: UserModelProtocol = get_user_model()

    def post(self, **fields) -> None:
        self.model.objects.create_user(**fields)
