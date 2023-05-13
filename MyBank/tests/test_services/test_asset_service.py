from django.conf import settings
from django.test import TestCase

from app.models import Asset, AssetCategory
from app.repositories import CRUDHandler, BulkHandler
from app.serializers import AssetSerializer
from app.services import AssetService
from app.services.model.asset import CurrencyUpdater, CurrencyRequester


class TestService(TestCase):
    """Testing AssetService objects."""

    @classmethod
    def setUpTestData(cls):
        for instance in (
            AssetCategory('currency', 'Валюты'),
            AssetCategory('moex_stock', 'Мосбиржа акции'),
        ):
            instance.save()
        cls.service = AssetService(
            CRUDHandler(Asset),  # type: ignore
            CurrencyUpdater(
                CurrencyRequester(settings.CURRENCIES_API_URL),
                BulkHandler(Asset)  # type: ignore
            ),
        )
        cls.get_serializer = AssetSerializer

    def test_init_update(self):
        self.service.updater(init=True)
        currencies = self.service.crud.get(
            serializer=self.get_serializer,
            many=True,
        )
        currencies = {i['name']: i for i in currencies}
        self.assertTrue(all([currencies.get('USD'), currencies.get('RUB'), currencies.get('BTC')]))

    def test_update_without_init(self):
        self.service.updater()
        currencies = self.service.crud.get(
            serializer=self.get_serializer,
            many=True,
        )
        self.assertTrue(currencies == [])

    def test_init_update_and_update_again(self):
        self.service.updater(init=True)
        currencies = self.service.crud.get(
            serializer=self.get_serializer,
            many=True,
        )
        currencies = {i['name']: i for i in currencies}
        self.assertTrue(all([currencies.get('USD'), currencies.get('RUB'), currencies.get('BTC')]))

        self.service.updater()
        currencies = self.service.crud.get(
            serializer=self.get_serializer,
            many=True,
        )
        currencies = {i['name']: i for i in currencies}
        self.assertTrue(all([currencies.get('USD'), currencies.get('RUB'), currencies.get('BTC')]))


