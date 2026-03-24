from rest_framework.test import APITestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from rest_framework import status
from api.auth.models import Profile

User = get_user_model()

class AuthViewsTestCase(APITestCase):

    def setUp(self):

        self.register_url = reverse('register')
        self.token_url = reverse('token_obtain_pair')
        self.logout_url = reverse('logout')
        self.account_url = reverse('account-list')

        self.user_data = {
            'name': 'Daniel',
            'email': 'daniel@example.com',
            'password': 'strongpassword123',
            'terms_of_use_is_ready': True
        }

        self.user = User.objects.create_user(
            name='Existing User',
            email='existing@example.com',
            password='password123',
            terms_of_use_is_ready=True
        )

    def test_register_view_creates_user_and_profile(self):

        response = self.client.post(self.register_url, self.user_data, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn('access', response.data)
        self.assertTrue(User.objects.filter(email=self.user_data['email']).exists())

        user = User.objects.get(email=self.user_data['email'])

        self.assertTrue(Profile.objects.filter(user=user).exists())

    def test_token_obtain_pair_view(self):

        response = self.client.post(self.token_url, {'email': self.user.email, 'password': 'password123'}, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertIn('access', response.data)
        self.assertIn('refresh', response.data)

    def test_logout_blacklists_token(self):

        response = self.client.post(self.token_url, {'email': self.user.email, 'password': 'password123'}, format='json')
        refresh_token = response.data['refresh']
        logout_response = self.client.post(self.logout_url, {'refresh_token': refresh_token}, format='json')

        self.assertEqual(logout_response.status_code, status.HTTP_205_RESET_CONTENT)

    def test_logout_with_invalid_token_returns_400(self):

        logout_response = self.client.post(self.logout_url, {'refresh_token': 'invalidtoken'}, format='json')

        self.assertEqual(logout_response.status_code, status.HTTP_400_BAD_REQUEST)
