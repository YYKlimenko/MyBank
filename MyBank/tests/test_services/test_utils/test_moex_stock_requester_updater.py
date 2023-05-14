from django.conf import settings
from django.test import TestCase

from app.models import AssetCategory, Asset
from app.repositories import BulkHandler, CRUDHandler
from app.serializers import AssetSerializer
from app.services.model import MoexStockRequester, MoexStockUpdater


class TestService(TestCase):
    """Testing MoexStock Requester&Updater objects."""

    @classmethod
    def setUpTestData(cls):
        instance = AssetCategory(name='moex_stock')
        instance.save()
        requester = MoexStockRequester(url=settings.MOEX_STOCK_API_URL)
        cls.updater = MoexStockUpdater(
            requester,
            BulkHandler(Asset),  # type: ignore
            category_id='moex_stock'
        )
        cls.requester = requester
        cls.crud = CRUDHandler(Asset)  # type: ignore
        cls.serializer = AssetSerializer

    def test_request_and_update(self):
        data = self.requester()
        self.assertTrue(all(['SBER' in data, 'BELU' in data, 'GAZP' in data]))
        self.updater(init=True, data=data)
        instances = self.crud.get(many=True, serializer=self.serializer)
        instances = {i['name']: i for i in instances}
        self.assertTrue(all([instances.get('SBER'), instances.get('BELU'), instances.get('GAZP')]))
