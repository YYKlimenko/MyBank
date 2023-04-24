from celery import shared_task

from .factories import CurrencyFactory


@shared_task(time_limit=1800)
def update():
    CurrencyFactory.get_service().updater()
