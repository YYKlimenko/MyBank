from django.conf import settings
from django.test import TestCase

from app.models import AssetCategory, Asset
from app.repositories import CRUDHandler
from app.serializers import AssetSerializer
from app.services.model import MoexStockRequester


class TestService(TestCase):
    """Testing MoexStock Requester objects."""

    @classmethod
    def setUpTestData(cls):
        instance = AssetCategory(name='moex_stock')
        instance.save()
        cls.requester = MoexStockRequester(url=settings.MOEX_STOCK_API_URL)
        cls.crud = CRUDHandler(Asset)  # type: ignore
        cls.serializer = AssetSerializer

    def test_request(self):
        data = self.requester()
        self.assertTrue(all(['SBER' in data, 'BELU' in data, 'GAZP' in data]))
