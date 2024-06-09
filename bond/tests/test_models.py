from datetime import date, timedelta
from decimal import Decimal

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.utils import timezone

from bond.models import Bond

User = get_user_model()


class BondModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(email='testuser', password='testpass')
        self.bond = Bond.objects.create(
            user=self.user,
            name="Test Bond",
            isin="CZ0003551251",
            value=1000.00,
            interest_rate=5.00,
            purchase_date=date(2023, 1, 1),
            maturity_date=date(2025, 1, 1),
            interest_payment_frequency="Annually"
        )

    def test_bond_creation(self):
        self.assertEqual(self.bond.name, "Test Bond")
        self.assertEqual(self.bond.isin, "CZ0003551251")
        self.assertEqual(self.bond.value, 1000.00)

    def test_bond_str(self):
        self.assertEqual(str(self.bond), self.bond.name)

    def test_future_value_two_years(self):
        bond = Bond(
            user=self.user,
            name='Test Bond',
            isin='TEST00000000',
            value=Decimal('999'),
            interest_rate=Decimal('5'),
            purchase_date=timezone.now().date(),
            maturity_date=timezone.now().date() + timedelta(days=2 * 365),
        )

        expected_fv = Decimal('999') * (Decimal('1') + Decimal('0.05')) ** Decimal('2')
        expected_future_value = expected_fv.quantize(Decimal('0.01'))

        self.assertAlmostEqual(bond.future_value, expected_future_value, places=2)

    def test_future_value_one_year_two_months_six_days(self):
        bond = Bond(
            user=self.user,
            name='Test Bond',
            isin='TEST00000000',
            value=Decimal('1659.97'),
            interest_rate=Decimal('5'),
            purchase_date=timezone.now().date(),
            maturity_date=timezone.now().date() + timedelta(days=365 + 2 * 30 + 6),
        )
        ytm = Decimal(365 + 2 * 30 + 6) / Decimal(365)
        expected_fv = Decimal('1659.97') * (Decimal('1') + Decimal('0.05')) ** ytm
        expected_future_value = expected_fv.quantize(Decimal('0.01'))

        self.assertAlmostEqual(bond.future_value, expected_future_value, places=2)

    def test_future_value_with_fractional_years(self):
        bond = Bond(
            user=self.user,
            name='Test Bond',
            isin='TEST00000000',
            value=Decimal('1000'),
            interest_rate=Decimal('5'),
            purchase_date=timezone.now().date(),
            maturity_date=timezone.now().date() + timedelta(days=400),
        )
        ytm = Decimal(400) / Decimal(365)
        expected_fv = Decimal('1000') * (Decimal('1') + Decimal('0.05')) ** ytm
        expected_future_value = expected_fv.quantize(Decimal('0.01'))

        self.assertAlmostEqual(bond.future_value, expected_future_value, places=2)
