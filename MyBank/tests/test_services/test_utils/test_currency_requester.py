from django.conf import settings
from django.test import TestCase

from app.services import CurrencyRequester


class TestService(TestCase):
    """Testing CurrencyRequester objects."""

    @classmethod
    def setUpTestData(cls):
        cls.requester = CurrencyRequester(url=settings.CURRENCIES_API_URL)

    def test_request(self):
        instances = self.requester()
        currencies = {key: instances[key] for key in instances}
        self.assertTrue(all([currencies.get('USD'), currencies.get('RUB'), currencies.get('CNY')]))
