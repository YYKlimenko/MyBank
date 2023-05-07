from _decimal import Decimal

from django.test import TestCase

from app.models import AssetCategory, Asset
from app.repositories import CRUDHandler
from app.serializers import AssetSerializer


class TestCRUDHandler(TestCase):
    """Testing CRUDHandler objects."""

    @classmethod
    def setUpTestData(cls):
        for instance in (
            AssetCategory('currency', 'Валюты'),
            AssetCategory('moex_stocks', 'Мосбиржа Акции'),
            Asset('USD', 'The United States of America', Decimal('75.88'), 'currency'),
            Asset('SBR', 'Sberbank', Decimal('240.00000'), 'moex_stocks'),
        ):
            instance.save()
        cls.crud_handler = CRUDHandler(Asset)  # type: ignore
        cls.get_serializer = AssetSerializer

    def test_get_all(self):
        assets = self.crud_handler.get(
            serializer=self.get_serializer,
            many=True,
        )
        expected_data = [
            {
                'name': 'USD',
                'description': 'The United States of America',
                'value': '75.88000',
                'category_id': 'currency',
                'user_id': None,
            },
            {
                'name': 'SBR',
                'description': 'Sberbank',
                'value': '240.00000',
                'category_id': 'moex_stocks',
                'user_id': None,
            },
        ]
        self.assertTrue(assets == expected_data)

    def test_get_one_by_pk(self):
        asset = self.crud_handler.get(
            serializer=self.get_serializer,
            many=False,
            name='USD',
        )
        expected_data = {
            'name': 'USD',
            'description': 'The United States of America',
            'value': '75.88000',
            'category_id': 'currency',
            'user_id': None,
        }
        self.assertTrue(asset == expected_data)

    def test_get_by_category(self):
        assets = self.crud_handler.get(
            serializer=self.get_serializer,
            many=True,
            category_id='currency',
        )
        expected_data = [{
            'name': 'USD',
            'description': 'The United States of America',
            'value': '75.88000',
            'category_id': 'currency',
            'user_id': None,
        }]
        self.assertTrue(assets == expected_data)

    def test_create(self):
        self.crud_handler.post(
            name='RUB',
            description='Russian Federation',
            value=Decimal('1.00000'),
            category_id='currency',
        )

        assets = self.crud_handler.get(
            serializer=self.get_serializer,
            many=True,
            category_id='currency',
        )
        expected_data = [
            {
             'name': 'USD',
             'description': 'The United States of America',
             'value': '75.88000',
             'category_id': 'currency',
             'user_id': None,
            },
            {
                'name': 'RUB',
                'description': 'Russian Federation',
                'value': '1.00000',
                'category_id': 'currency',
                'user_id': None,
            },
        ]
        self.assertTrue(assets == expected_data)

    def test_update(self):
        self.crud_handler.update(pk='USD', data={'value': Decimal('80.00000')})

        assets = self.crud_handler.get(
            serializer=self.get_serializer,
            many=False,
            name='USD',
        )
        expected_data = {
            'name': 'USD',
            'description': 'The United States of America',
            'value': '80.00000',
            'category_id': 'currency',
            'user_id': None,
        }

        self.assertTrue(assets == expected_data)

    def test_delete(self):
        self.crud_handler.delete(pk='USD')

        users = self.crud_handler.get(
            serializer=self.get_serializer,
            many=True,
        )
        self.assertTrue(
            users == [
                {
                 'name': 'SBR',
                 'description': 'Sberbank',
                 'value': '240.00000',
                 'category_id': 'moex_stocks',
                 'user_id': None,
                },
            ]
        )

