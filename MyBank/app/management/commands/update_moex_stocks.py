from django.core.management import BaseCommand

from app.factories import StockFactory


class Command(BaseCommand):
    def handle(self, **options):
        StockFactory.get_service().update()
