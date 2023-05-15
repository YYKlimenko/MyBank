from _decimal import Decimal

from django.conf import settings
from django.test import TestCase

from app.models import Asset, AssetCategory
from app.repositories import BulkHandler, CRUDHandler
from app.serializers import AssetSerializer
from app.services import CurrencyRequester, CurrencyUpdater


class TestService(TestCase):
    """Testing CurrencyUpdater objects."""

    @classmethod
    def setUpTestData(cls):
        for instance in (
            AssetCategory('currency', 'Валюты'),
        ):
            instance.save()
        cls.updater = CurrencyUpdater(
            CurrencyRequester(url=settings.CURRENCIES_API_URL),
            BulkHandler(Asset),  # type: ignore
        )
        cls.crud_handler = CRUDHandler(Asset)  # type: ignore
        cls.serializer = AssetSerializer

    def test_update(self):
        self.updater(init=True, data={'USD': Decimal('75.000'), 'RUB':  Decimal('1.00000'), 'CNY': Decimal('10')})
        expected_data = [
            {
                'name': 'USD',
                'description': None,
                'value': '75.00000',
                'category_id': 'currency',
                'user_id': None,
            },
            {
                'name': 'RUB',
                'description': None,
                'value': '1.00000',
                'category_id': 'currency',
                'user_id': None,
            },
            {
                'name': 'CNY',
                'description': None,
                'value': '10.00000',
                'category_id': 'currency',
                'user_id': None,
            },
        ]
        instances = self.crud_handler.get(serializer=self.serializer, many=True)
        self.assertTrue(instances == expected_data)

        self.updater(data={'USD': Decimal('100.000')})
        expected_data = [
            {
                'name': 'USD',
                'description': None,
                'value': '100.00000',
                'category_id': 'currency',
                'user_id': None,
            },
            {
                'name': 'RUB',
                'description': None,
                'value': '1.00000',
                'category_id': 'currency',
                'user_id': None,
            },
            {
                'name': 'CNY',
                'description': None,
                'value': '10.00000',
                'category_id': 'currency',
                'user_id': None,
            },
        ]
        instances = self.crud_handler.get(serializer=self.serializer, many=True)
        self.assertTrue(instances == expected_data)
