from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from .models import Restaurant

User = get_user_model()


class RestaurantTests(APITestCase):
    @classmethod
    def setUpTestData(cls):
        # Create a test user
        cls.admin_user = User.objects.create_superuser(
            email='admin@example.com',
            password='admin123'
        )

        # Create a test restaurant
        cls.restaurant = Restaurant.objects.create(
            name='Test Restaurant',
            address='123 Test St'
        )

    def test_create_restaurant(self):
        self.client.login(email='admin@example.com', password='admin123')
        url = reverse('restaurant-create')
        data = {
            'name': 'New Test Restaurant',
            'address': '123 New Test St'
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Restaurant.objects.count(), 2)
        self.assertEqual(Restaurant.objects.get(id=2).name, 'New Test Restaurant')

    def test_list_restaurants(self):
        url = reverse('restaurant-list')
        response = self.client.get(url)
        self.assertEqual(response.status_data, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['name'], 'Test Restaurant')

    def test_unauthorized_create_restaurant(self):
        url = reverse('restaurant-create')
        data = {
            'name': 'Unauthorized Restaurant',
            'address': '404 Nowhere St'
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
