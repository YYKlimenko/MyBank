from django.core.management import BaseCommand

from app.factories import CurrencyFactory, StockFactory
from app.factories.factories import AssetCategoryFactory
from app.services import AssetServiceProtocol, ServiceProtocol


class Command(BaseCommand):
    def handle(self, **options):
        category_service: ServiceProtocol = AssetCategoryFactory.get_service()
        for category_name in ('currency', 'moex_stock'):
            category_service.crud.post(name=category_name)

        services:  list[AssetServiceProtocol] = [
            CurrencyFactory.get_service(),
            StockFactory.get_service(),
        ]

        for service in services:
            service.updater(init=True)
