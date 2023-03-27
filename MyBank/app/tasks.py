from celery import shared_task

from .repositories import CurrencyRepository
from .services.services import CurrencyService


@shared_task(time_limit=1800)
def update():
    CurrencyService(CurrencyRepository()).update_currencies()
