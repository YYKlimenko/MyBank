from _decimal import Decimal

from django.contrib.auth import get_user_model
from django.test import TestCase

from app.models import Asset, Property, Account, AssetCategory
from app.repositories.model import UserCounter
from app.serializers.model import CreatingUserSerializer


class TestUserCounter(TestCase):
    """Testing UserCRUDHandler objects."""

    @classmethod
    def setUpTestData(cls):
        user = CreatingUserSerializer(
            data={
                'password': 'user',
                'password2': 'user',
                'username': 'user',
                'first_name': 'Sergey',
                'last_name': 'Sergeev',
                'email': 'sergey@sergeev.com',
            }
        )
        user.is_valid()

        for instance in (
                get_user_model()(** user.validated_data),
                AssetCategory('currency', 'Валюты'),
                Asset('USD', 'The United State of America', '75.88', 'currency', 1),
                Property(user_id=1, name='The car', description='My favorite car', value='750000'),
                Account(name='currency', asset_id='USD', user_id=1, count=2000),
        ):
            instance.save()

        cls.user_counter = UserCounter(get_user_model())

    def test_get_sum(self):
        result = self.user_counter.get_sum(1)
        expected_data = {'username': 'user', 'sum_account': Decimal('151760'), 'sum_properties': Decimal('750000')}
        self.assertTrue(result == expected_data)

    def test_get_sum_for_non_existed_user(self):
        result = self.user_counter.get_sum(2)
        expected_data = {}
        self.assertTrue(result == expected_data)
