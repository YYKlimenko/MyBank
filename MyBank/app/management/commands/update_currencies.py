from django.core.management import BaseCommand

from app.repositories import CurrencyRepository
from app.services.services import CurrencyService


class Command(BaseCommand):
    def handle(self, **options):
        CurrencyService(CurrencyRepository()).update_currencies()
