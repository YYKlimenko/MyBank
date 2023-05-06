from django.contrib.auth import get_user_model
from django.test import TestCase

from app.serializers.model import CreatingUserSerializer


class AuthTest(TestCase):
    """Testing User views."""

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

    def test_get_token(self):
        response = self.client.post(
            'http://127.0.0.1:8000/api/v1/token/',
            {'username': 'user', 'password': 'user'}
        )
        self.assertTrue(response.status_code == 200)
        self.assertTrue(isinstance(response.data, dict))
        self.assertTrue(response.data.get('access', False))
        self.assertTrue(response.data.get('refresh', False))

    def test_get_token_with_invalid_data(self):
        response = self.client.post(
            'http://127.0.0.1:8000/api/v1/token/',
            {'username': 'admin2', 'password': 'admin'}
        )
        self.assertTrue(response.status_code == 401)
