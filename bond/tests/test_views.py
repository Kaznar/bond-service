from datetime import date

from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework.test import APITestCase, APIClient

from bond.models import Bond

User = get_user_model()


class BondViewSetTest(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(email='testuser', password='testpass')
        self.client.force_authenticate(user=self.user)
        self.bond = Bond.objects.create(
            user=self.user,
            name="Apple Bond",
            isin="CZ0003551251",
            value=2000.00,
            interest_rate=4.00,
            purchase_date=date(2023, 2, 1),
            maturity_date=date(2026, 2, 1),
            interest_payment_frequency="Semi-Annually"
        )
        self.bond_url = reverse('bond-detail', kwargs={'pk': self.bond.pk})

    def test_retrieve_bond(self):
        response = self.client.get(self.bond_url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['name'], self.bond.name)

    def test_list_bonds(self):
        response = self.client.get(reverse('bond-list-create'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)

    def test_create_duplicate_bond(self):
        data = {
            'name': "Test Bond",
            'isin': "CZ0001007306",  # unique
            'value': 2000.00,
            'interest_rate': 4.00,
            'purchase_date': date(2023, 2, 1),
            'maturity_date': date(2026, 2, 1),
            'interest_payment_frequency': "Semi-Annually"
        }
        response = self.client.post(reverse('bond-list-create'), data, format='json')
        self.assertEqual(response.status_code, 201)

        response = self.client.post(reverse('bond-list-create'), data, format='json')
        self.assertEqual(response.status_code, 400)

    def test_update_bond(self):
        data = {
            'name': "Updated Bond",
            'isin': self.bond.isin,
            'value': 1500.00,
            'interest_rate': 4.50,
            'purchase_date': self.bond.purchase_date,
            'maturity_date': self.bond.maturity_date,
            'interest_payment_frequency': self.bond.interest_payment_frequency
        }
        response = self.client.put(self.bond_url, data, format='json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['name'], data['name'])

    def test_partial_update_bond(self):
        data = {'value': '1200.00'}
        response = self.client.patch(self.bond_url, data, format='json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['value'], data['value'])

    def test_delete_bond(self):
        response = self.client.delete(self.bond_url)
        self.assertEqual(response.status_code, 204)
