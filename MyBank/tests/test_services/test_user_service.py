from _decimal import Decimal

from django.contrib.auth import get_user_model
from django.test import TestCase

from app.models import AssetCategory, Asset, Property, Account
from app.repositories.model import UserCRUDHandler, UserCounter
from app.serializers.model import CreatingUserSerializer, UserSerializer
from app.serializers.protocols import SerializerProtocol
from app.services import UserService


class TestUserCRUDHandler(TestCase):
    """Testing UserService objects."""

    @classmethod
    def setUpTestData(cls):
        user_model = get_user_model()

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
                get_user_model()(**user.validated_data),
                AssetCategory('currency', 'Валюты'),
                Asset('USD', 'The United State of America', '75.88', 'currency', 1),
                Property(user_id=1, name='The car', description='My favorite car', value='750000'),
                Account(name='currency', asset_id='USD', user_id=1, count=2000),
        ):
            instance.save()

        cls.user_model = user_model
        cls.service = UserService(
            UserCRUDHandler(get_user_model()),
            UserCounter(get_user_model()),
        )
        cls.get_serializer: SerializerProtocol = UserSerializer
        cls.post_serializer: SerializerProtocol = CreatingUserSerializer

    def test_get_all(self):
        users = self.service.crud.get(
            serializer=self.get_serializer,
            many=True,
        )
        data = [{
                 'id': 1,
                 'username': 'user',
                 'first_name': 'Sergey',
                 'last_name': 'Sergeev',
                 'email': 'sergey@sergeev.com',
                 'is_active': True,
        }]
        self.assertTrue(users == data)

    def test_get_one_by_id(self):
        users = self.service.crud.get(
            serializer=self.get_serializer,
            many=False,
            id=1,
        )
        data = {
                'id': 1,
                'username': 'user',
                'first_name': 'Sergey',
                'last_name': 'Sergeev',
                'email': 'sergey@sergeev.com',
                'is_active': True,
            }
        self.assertTrue(users == data)

    def test_get_one_by_username(self):
        users = self.service.crud.get(
            serializer=self.get_serializer,
            many=False,
            username='user',
        )
        data = {
                'id': 1,
                'username': 'user',
                'first_name': 'Sergey',
                'last_name': 'Sergeev',
                'email': 'sergey@sergeev.com',
                'is_active': True,
            }
        self.assertTrue(users == data)

    def test_create(self):
        user = self.post_serializer(
            data={
                'password': 'user2',
                'password2': 'user2',
                'username': 'user2',
                'first_name': 'Ivan',
                'last_name': 'Ivanov',
                'email': 'ivan@ivanov.ru',
            }
        )
        user.is_valid()
        self.service.crud.post(**user.validated_data)

        users = self.service.crud.get(
            serializer=self.get_serializer,
            many=True,
        )
        data = [
            {
             'id': 1,
             'username': 'user',
             'first_name': 'Sergey',
             'last_name': 'Sergeev',
             'email': 'sergey@sergeev.com',
             'is_active': True,
            },
            {
                'id': 2,
                'username': 'user2',
                'first_name': 'Ivan',
                'last_name': 'Ivanov',
                'email': 'ivan@ivanov.ru',
                'is_active': True,
            },
        ]
        self.assertTrue(users == data)

    def test_update(self):
        self.service.crud.update(pk=1, data={'first_name': 'New Sergey'})

        users = self.service.crud.get(
            serializer=self.get_serializer,
            many=False,
            id=1,
        )
        data = {
            'id': 1,
            'username': 'user',
            'first_name': 'New Sergey',
            'last_name': 'Sergeev',
            'email': 'sergey@sergeev.com',
            'is_active': True,
        }

        self.assertTrue(users == data)

    def test_delete(self):
        self.service.crud.delete(pk=1)

        users = self.service.crud.get(
            serializer=self.get_serializer,
            many=True,
        )
        self.assertTrue(users == [])

    def test_get_sum(self):
        result = self.service.counter.get_sum(1)
        expected_data = {'username': 'user', 'sum_account': Decimal('151760'), 'sum_properties': Decimal('750000')}
        self.assertTrue(result == expected_data)

    def test_get_sum_for_non_existed_user(self):
        result = self.service.counter.get_sum(2)
        expected_data = {}
        self.assertTrue(result == expected_data)
