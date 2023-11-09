from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

User = get_user_model()


class AuthenticationTests(APITestCase):
    def test_user_registration(self):
        url = reverse('user-register')
        data = {'email': 'test@example.com', 'password': 'testpassword123'}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn('access', response.data)

    def test_user_login(self):
        User.objects.create_user(email='login@test.com', password='test-login')
        url = reverse('user-login')
        data = {'email': 'login@test.com', 'password': 'test-login'}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('access', response.data)
