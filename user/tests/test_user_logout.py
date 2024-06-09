from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

User = get_user_model()


class UserLogoutTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.logout_url = reverse('rest_logout')
        self.user = User.objects.create_user(email='testuser@example.com',
                                             password='strongpassword123')
        self.client.login(email='testuser@example.com', password='strongpassword123')

    def test_user_logout(self):
        response = self.client.post(self.logout_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
