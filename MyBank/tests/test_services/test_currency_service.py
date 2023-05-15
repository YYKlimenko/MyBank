from _decimal import Decimal

from django.conf import settings
from django.test import TestCase

from app.models import Asset, AssetCategory
from app.repositories import CRUDHandler, BulkHandler, FieldError
from app.serializers import AssetSerializer
from app.services import AssetService
from app.services.model.asset import CurrencyUpdater, CurrencyRequester


class TestService(TestCase):
    """Testing Currency Service objects."""

    @classmethod
    def setUpTestData(cls):
        for instance in (
            AssetCategory('currency', 'Валюты'),
            Asset(name='AAA', value=Decimal('75.5'), category_id='currency'),
            Asset(name='BBB', value=Decimal('1.0'), category_id='currency'),
        ):
            instance.save()
        cls.service = AssetService(
            CRUDHandler(Asset),  # type: ignore
            CurrencyUpdater(
                CurrencyRequester(settings.CURRENCIES_API_URL),
                BulkHandler(Asset)  # type: ignore
            ),
        )
        cls.get_serializer = AssetSerializer

    def test_get_all(self):
        currencies = self.service.crud.get(
            serializer=self.get_serializer,
            many=True,
        )
        expected_data = [
            {
                'name': 'AAA',
                'description': None,
                'value': '75.50000',
                'category_id': 'currency',
                'user_id': None,
            },
            {
                'name': 'BBB',
                'description': None,
                'value': '1.00000',
                'category_id': 'currency',
                'user_id': None,
            },
        ]
        self.assertTrue(currencies == expected_data)

    def test_get_one_by_pk(self):
        currency = self.service.crud.get(
            serializer=self.get_serializer,
            many=False,
            name='AAA',
        )
        expected_data = {
                'name': 'AAA',
                'description': None,
                'value': '75.50000',
                'category_id': 'currency',
                'user_id': None,
        }
        self.assertTrue(currency == expected_data)

    def test_get_by_field(self):
        currency = self.service.crud.get(
            serializer=self.get_serializer,
            many=True,
            value='75.500',
        )
        expected_data = [{
                'name': 'AAA',
                'description': None,
                'value': '75.50000',
                'category_id': 'currency',
                'user_id': None,
        }]
        self.assertTrue(currency == expected_data)

    def test_get_by_invalid_field(self):
        with self.assertRaises(FieldError) as raised:
            self.service.crud.get(
                serializer=self.get_serializer,
                many=True,
                last_name='Klimenko',
            )
        self.assertTrue(isinstance(raised.exception, FieldError))

    def test_create(self):
        self.service.crud.post(
            name='CCC',
            value=Decimal('700000.000'),
            category_id='currency',
        )

        currencies = self.service.crud.get(
            serializer=self.get_serializer,
            many=True,
        )
        expected_data = [
            {
                'name': 'AAA',
                'description': None,
                'value': '75.50000',
                'category_id': 'currency',
                'user_id': None,
            },
            {
                'name': 'BBB',
                'description': None,
                'value': '1.00000',
                'category_id': 'currency',
                'user_id': None,
            },
            {
                'name': 'CCC',
                'description': None,
                'value': '700000.00000',
                'category_id': 'currency',
                'user_id': None,
            },
        ]
        self.assertTrue(currencies == expected_data)

    def test_update(self):
        self.service.crud.update(pk='AAA', data={'description': 'Currency of AAA'})

        currency = self.service.crud.get(
            serializer=self.get_serializer,
            many=False,
            name='AAA',
        )
        expected_data = {
            'name': 'AAA',
            'description': 'Currency of AAA',
            'value': '75.50000',
            'category_id': 'currency',
            'user_id': None,
        }
        self.assertTrue(currency == expected_data)

    def test_update_non_existed_instance(self):
        self.service.crud.update(pk='DDD', data={'description': 'Currency of AAA'})

        currency = self.service.crud.get(
            serializer=self.get_serializer,
            many=True,
        )
        expected_data = [
            {
                'name': 'AAA',
                'description': None,
                'value': '75.50000',
                'category_id': 'currency',
                'user_id': None,
            },
            {
                'name': 'BBB',
                'description': None,
                'value': '1.00000',
                'category_id': 'currency',
                'user_id': None,
            },
        ]
        self.assertTrue(currency == expected_data)

    def test_update_with_incorrect_field(self):
        with self.assertRaises(FieldError) as raised:
            self.service.crud.update(pk='AAA', data={'text': 'Currency of AAA'})
        self.assertTrue(isinstance(raised.exception, FieldError))

    def test_update_with_incorrect_type_of_field(self):
        with self.assertRaises(FieldError) as raised:
            self.service.crud.update(pk='AAA', data={'user_id': 'Yura'})
        self.assertTrue(isinstance(raised.exception, FieldError))

    def test_delete(self):
        self.service.crud.delete(pk='BBB')

        currencies = self.service.crud.get(
            serializer=self.get_serializer,
            many=True,
        )
        self.assertTrue(
            currencies == [
                {
                    'name': 'AAA',
                    'description': None,
                    'value': '75.50000',
                    'category_id': 'currency',
                    'user_id': None,
                },
            ]
        )

    def test_init_update_and_update_again(self):
        self.service.updater(init=True, data={'CNY': Decimal('12.00000')})
        currencies = self.service.crud.get(
            serializer=self.get_serializer,
            many=True,
        )
        expected_data = [
            {
                'name': 'AAA',
                'description': None,
                'value': '75.50000',
                'category_id': 'currency',
                'user_id': None,
            },
            {
                'name': 'BBB',
                'description': None,
                'value': '1.00000',
                'category_id': 'currency',
                'user_id': None,
            },
            {
                'name': 'CNY',
                'description': None,
                'value': '12.00000',
                'category_id': 'currency',
                'user_id': None,
            },
        ]
        self.assertTrue(currencies == expected_data)

        self.service.updater(data={'AAA': '999.99999'})
        currencies = self.service.crud.get(
            serializer=self.get_serializer,
            many=True,
        )
        expected_data = [
            {
                'name': 'AAA',
                'description': None,
                'value': '999.99999',
                'category_id': 'currency',
                'user_id': None,
            },
            {
                'name': 'BBB',
                'description': None,
                'value': '1.00000',
                'category_id': 'currency',
                'user_id': None,
            },
            {
                'name': 'CNY',
                'description': None,
                'value': '12.00000',
                'category_id': 'currency',
                'user_id': None,
            },
        ]
        self.assertTrue(currencies == expected_data)
