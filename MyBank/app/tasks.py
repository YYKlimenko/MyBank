import requests
from django.conf import settings
from .models import Currency
from celery import shared_task


@shared_task(time_limit=1800)
def update_btc():
    response = requests.get(settings.CURRENCIES_API_URL)
    actual_currencies = response.json()['rates']
    rub = actual_currencies['RUB']
    db_currencies = Currency.objects.filter(name__in=['BTC', 'EUR', 'CNY', 'USD'])

    for db_currency in db_currencies:
        if db_currency.name == 'USD':
            db_currency.value = rub
        else:
            db_currency.value = 1 / actual_currencies[db_currency.name] * rub
        Currency.save(db_currency)
