from django.conf import settings
from django.test import TestCase

from app.models import AssetCategory, Asset
from app.repositories import BulkHandler, CRUDHandler
from app.serializers import AssetSerializer
from app.services.model import MoexStockRequester, MoexStockUpdater


class TestService(TestCase):
    """Testing MoexStock Updater objects."""

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

    def test_update(self):
        self.updater(init=True, data={'SBER': '235', 'BELU': '100'})
        instances = self.crud.get(many=True, serializer=self.serializer)
        expected_data = [
            {
                'name': 'SBER',
                'description': 'SBER',
                'value': '235.00000',
                'category_id': 'moex_stock',
                'user_id': None,
            },
            {
                'name': 'BELU',
                'description': 'BELU',
                'value': '100.00000',
                'category_id': 'moex_stock',
                'user_id': None,
            },
        ]

        self.assertTrue(instances == expected_data)
        self.updater(data={'SBER': '100', 'BELU': '235'})

        expected_data = [
            {
                'name': 'SBER',
                'description': 'SBER',
                'value': '100.00000',
                'category_id': 'moex_stock',
                'user_id': None,
            },
            {
                'name': 'BELU',
                'description': 'BELU',
                'value': '235.00000',
                'category_id': 'moex_stock',
                'user_id': None,
            },
        ]
        instances = self.crud.get(many=True, serializer=self.serializer)
        self.assertTrue(instances == expected_data)
