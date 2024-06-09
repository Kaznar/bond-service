from datetime import date

from django.contrib.auth import get_user_model
from rest_framework.test import APITestCase

from bond.models import Bond
from bond.serializers import BondSerializer

User = get_user_model()


class BondSerializerTest(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(email='testuser', password='testpass')
        self.bond_data = {
            'name': "Test Bond",
            'isin': "CZ0003551251",
            'value': 1000.00,
            'interest_rate': 5.00,
            'purchase_date': date(2023, 1, 1),
            'maturity_date': date(2025, 1, 1),
            'interest_payment_frequency': "Annually"

        }
        self.serializer = BondSerializer(data=self.bond_data)

    def test_serializer_validation(self):
        self.assertTrue(self.serializer.is_valid())

    def test_isin_validation(self):
        invalid_data = self.bond_data.copy()
        invalid_data['isin'] = 'INVALIDISIN'
        serializer = BondSerializer(data=invalid_data)
        self.assertFalse(serializer.is_valid())
        self.assertIn('isin', serializer.errors)

    def test_missing_fields(self):
        required_fields = ['name', 'isin', 'value', 'interest_rate', 'purchase_date',
                           'maturity_date', 'interest_payment_frequency']
        for field in required_fields:
            data = self.bond_data.copy()
            data.pop(field)
            serializer = BondSerializer(data=data)
            self.assertFalse(serializer.is_valid())
            self.assertIn(field, serializer.errors)

    def test_field_types(self):
        invalid_data = self.bond_data.copy()
        invalid_data['value'] = 'not_a_number'
        serializer = BondSerializer(data=invalid_data)
        self.assertFalse(serializer.is_valid())
        self.assertIn('value', serializer.errors)
