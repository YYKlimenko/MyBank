from typing import Any

from django.db.models import Sum, F  # type: ignore

from app.models.protocols import UserModelProtocol
from app.repositories import CRUDHandler


class UserCrudHandler(CRUDHandler):
    model: UserModelProtocol

    def post(self, **fields) -> None:
        self.model.objects.create_user(**fields)


class UserCounter:

    def __init__(self, user_model: UserModelProtocol):
        self.model = user_model

    def get_sum(self, user_id: int) -> dict[str, Any]:
        user = self.model.objects.filter(id=user_id).only('username').prefetch_related().annotate(
            sum_accounts=Sum(F('accounts__asset__value') * F('accounts__count')),
            sum_properties=Sum('properties__value'),
        )[0]
        return {
            'username': user.username,
            'sum_account': user.sum_accounts,
            'sum_properties': user.sum_properties,
        }
