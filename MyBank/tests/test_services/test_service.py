from django.test import TestCase

from app.models import AssetCategory
from app.repositories import CRUDHandler, FieldError
from app.serializers import AssetCategorySerializer
from app.services import Service


class TestService(TestCase):
    """Testing Service objects."""

    @classmethod
    def setUpTestData(cls):
        for instance in (
            AssetCategory('currency', 'Валюты'),
            AssetCategory('moex_stock', 'Мосбиржа акции'),
        ):
            instance.save()
        cls.service = Service(CRUDHandler(AssetCategory))  # type: ignore
        cls.get_serializer = AssetCategorySerializer

    def test_get_all(self):
        categories = self.service.crud.get(
            serializer=self.get_serializer,
            many=True,
        )
        expected_data = [
            {
                'name': 'currency',
                'verbose_name': 'Валюты',
                'description': None,
            },
            {
                'name': 'moex_stock',
                'verbose_name': 'Мосбиржа акции',
                'description': None,
            },
        ]
        self.assertTrue(categories == expected_data)

    def test_get_one_by_pk(self):
        categories = self.service.crud.get(
            serializer=self.get_serializer,
            many=False,
            name='currency',
        )
        expected_data = {
            'name': 'currency',
            'verbose_name': 'Валюты',
            'description': None,
        }
        self.assertTrue(categories == expected_data)

    def test_get_by_field(self):
        categories = self.service.crud.get(
            serializer=self.get_serializer,
            many=True,
            verbose_name='Валюты',
        )
        expected_data = [{
            'name': 'currency',
            'verbose_name': 'Валюты',
            'description': None,
        }]
        self.assertTrue(categories == expected_data)

    def test_get_by_invalid_field(self):
        with self.assertRaises(FieldError) as raised:
            self.service.crud.get(
                serializer=self.get_serializer,
                many=True,
                value=130,
            )

        self.assertTrue(isinstance(raised.exception, FieldError))

    def test_create(self):
        self.service.crud.post(
            name='moex_bond',
            verbose_name='Мосбиржа облигации',
        )

        categories = self.service.crud.get(
            serializer=self.get_serializer,
            many=True,
        )
        expected_data = [
            {
                'name': 'currency',
                'verbose_name': 'Валюты',
                'description': None,
            },
            {
                'name': 'moex_stock',
                'verbose_name': 'Мосбиржа акции',
                'description': None,
            },
            {
                'name': 'moex_bond',
                'verbose_name': 'Мосбиржа облигации',
                'description': None,
            },
        ]
        self.assertTrue(categories == expected_data)

    def test_update(self):
        self.service.crud.update(pk='currency', data={'description': 'Деньги, используемые в странах мира'})

        categories = self.service.crud.get(
            serializer=self.get_serializer,
            many=False,
            name='currency',
        )
        expected_data = {
            'name': 'currency',
            'verbose_name': 'Валюты',
            'description': 'Деньги, используемые в странах мира',
        }
        self.assertTrue(categories == expected_data)

    def test_delete(self):
        self.service.crud.delete(pk='moex_stock')

        categories = self.service.crud.get(
            serializer=self.get_serializer,
            many=True,
        )
        self.assertTrue(
            categories == [
                {
                    'name': 'currency',
                    'verbose_name': 'Валюты',
                    'description': None,
                },
            ]
        )
