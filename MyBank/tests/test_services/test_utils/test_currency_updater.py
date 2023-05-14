from _decimal import Decimal

from django.conf import settings
from django.test import TestCase

from app.models import Asset, AssetCategory
from app.repositories import BulkHandler, CRUDHandler
from app.serializers import AssetSerializer
from app.services import CurrencyRequester, CurrencyUpdater


class TestService(TestCase):
    """Testing UpdaterRequester objects."""

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

    def test_request(self):
        self.updater(init=True, data={'USD': Decimal('75.000'), 'RUB':  Decimal('1.00000'), 'CNY': Decimal('10')})
        instances = self.crud_handler.get(serializer=self.serializer, many=True)
        instances = {i['name']: i for i in instances}
        self.assertTrue(all([instances.get('USD'), instances.get('RUB'), instances.get('CNY')]))
