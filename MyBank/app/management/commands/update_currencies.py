from django.core.management import BaseCommand

from app.factories import CurrencyFactory


class Command(BaseCommand):
    def handle(self, **options):
        CurrencyFactory.get_service().update()
