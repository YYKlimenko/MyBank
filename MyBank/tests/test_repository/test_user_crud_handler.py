from django.contrib.auth import get_user_model
from django.test import TestCase

from app.repositories.model import UserCRUDHandler
from app.serializers.model import CreatingUserSerializer, UserSerializer
from app.serializers.protocols import SerializerProtocol


class TestUserCRUDHandler(TestCase):
    """Testing UserCRUDHandler objects."""

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
        user = user_model(**user.validated_data)
        user.save()

        cls.user_model = user_model
        cls.user_crud_handler = UserCRUDHandler(get_user_model())
        cls.get_serializer: SerializerProtocol = UserSerializer
        cls.post_serializer: SerializerProtocol = CreatingUserSerializer

    def test_get_all(self):
        users = self.user_crud_handler.get(
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
        users = self.user_crud_handler.get(
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
        users = self.user_crud_handler.get(
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
        self.user_crud_handler.post(**user.validated_data)

        users = self.user_crud_handler.get(
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
        self.user_crud_handler.update(pk=1, data={'first_name': 'New Sergey'})

        users = self.user_crud_handler.get(
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
        self.user_crud_handler.delete(pk=1)

        users = self.user_crud_handler.get(
            serializer=self.get_serializer,
            many=True,
        )
        self.assertTrue(users == [])
