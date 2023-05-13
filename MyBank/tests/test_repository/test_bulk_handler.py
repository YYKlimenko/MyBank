from _decimal import Decimal

from django.test import TestCase

from app.models import AssetCategory, Asset
from app.repositories import BulkHandler, CRUDHandler
from app.repositories.exceptions import FieldError
from app.serializers import AssetSerializer


class TestBulkHandler(TestCase):
    """Testing BulkHandler objects."""

    @classmethod
    def setUpTestData(cls):
        for instance in (
            AssetCategory('currency', 'Валюты'),
            AssetCategory('moex_stocks', 'Мосбиржа Акции'),
            Asset('SBR', 'Sberbank', Decimal('240.00000'), 'moex_stocks'),
        ):
            instance.save()
        cls.crud_handler = CRUDHandler(Asset)  # type: ignore
        cls.bulk_handler = BulkHandler(Asset)  # type: ignore
        cls.get_serializer = AssetSerializer

    def test_bulk_create(self):
        self.bulk_handler.create({
            'RUB': {
                'description': 'Russian Federation',
                'value': Decimal('1.00000'),
                'category_id': 'currency',
             },
            'USD': {
                'description': 'The United States of America',
                'value': Decimal('75.88000'),
                'category_id': 'currency',
            },
        })

        assets = self.crud_handler.get(
            serializer=self.get_serializer,
            many=True,
        )
        expected_data = [
            {
                'name': 'SBR',
                'description': 'Sberbank',
                'value': '240.00000',
                'category_id': 'moex_stocks',
                'user_id': None,
            },
            {
                'name': 'RUB',
                'description': 'Russian Federation',
                'value': '1.00000',
                'category_id': 'currency',
                'user_id': None,
            },
            {
                'name': 'USD',
                'description': 'The United States of America',
                'value': '75.88000',
                'category_id': 'currency',
                'user_id': None,
            },
        ]
        self.assertTrue(assets == expected_data)

    def test_bulk_update(self):
        self.bulk_handler.update(
            {
                'SBR':
                {
                    'description': 'Sberbank',
                    'value': Decimal('245.00000'),
                    'category_id': 'moex_stocks',
                    'user_id': None,
                },
            },
            fields=['description', 'value', 'category_id', 'user_id'],
        )

        assets = self.crud_handler.get(
            serializer=self.get_serializer,
            many=True,
        )
        expected_data = [
            {
                'name': 'SBR',
                'description': 'Sberbank',
                'value': '245.00000',
                'category_id': 'moex_stocks',
                'user_id': None,
            },
        ]
        self.assertTrue(assets == expected_data)

    def test_bulk_create_with_invalid_data(self):
        with self.assertRaises(FieldError) as raised:
            self.bulk_handler.create({'category': 'RUB'})
        self.assertTrue(isinstance(raised.exception, FieldError))

    def test_bulk_update_with_invalid_data(self):
        with self.assertRaises(FieldError) as raised:
            self.bulk_handler.update(
                {
                    'SBR':
                        {
                            'descrip': 'Sberbank',
                        },
                },
                fields=['description', 'value', 'category_id', 'user_id'],
            )
        self.assertTrue(isinstance(raised.exception, FieldError))
