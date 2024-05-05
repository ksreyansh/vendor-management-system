from django.test import TestCase
from django.contrib.auth import get_user_model
from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase, APIClient
from django.urls import reverse
from rest_framework import status

from .models import CustomUser
from .views import UserLoginView


# Create your tests here.
class UserManagerTests(TestCase):
    def test_create_user(self):
        User = get_user_model()
        user = User.objects.create_user(email="normal@user.com", password="123")
        self.assertEqual(user.email, "normal@user.com")
        self.assertTrue(user.is_active)
        self.assertFalse(user.is_staff)
        self.assertFalse(user.is_superuser)

        try:
            self.assertIsNone(user.username)
        except AttributeError:
            pass
        with self.assertRaises(TypeError):
            User.objects.create_user()
        with self.assertRaises(TypeError):
            User.objects.create_user(email="")
        with self.assertRaises(ValueError):
            User.objects.create_user(email="", password="123")

        print("Test: Create user -> Completed")

    def test_create_superuser(self):
        User = get_user_model()
        admin_user = User.objects.create_superuser(email="super@user.com", password="123")
        self.assertEqual(admin_user.email, "super@user.com")
        self.assertTrue(admin_user.is_active)
        self.assertTrue(admin_user.is_staff)
        self.assertTrue(admin_user.is_superuser)
        try:
            self.assertIsNone(admin_user.username)
        except AttributeError:
            pass
        with self.assertRaises(ValueError):
            User.objects.create_superuser(email="super@user.com", password="123", is_superuser=False)

        print("Test: Create superuser -> Completed")


class AuthenticateAPITestCase(APITestCase):
    def setUp(self):
        self.user = CustomUser.objects.create_user(email="testuser@user.com", password="password123")
        self.token = Token.objects.create(user=self.user)

    def test_login_success(self):
        url = reverse("auth:login")
        data = {'email': 'testuser@user.com', 'password': 'password123'}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('token', response.data)

        print("Test: Login successful -> Completed")

    def test_login_failure_invalid_credentials(self):
        url = reverse("auth:login")
        data = {'email': 'testuser@user.com', 'password': 'password'}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertIn('error', response.data)

        print("Test: Login failure due to invalid credentials -> Completed")

    def test_login_failure_missing_credentials(self):
        url = reverse("auth:login")
        data = {'email': 'testuser@user.com'}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        print("Test: Login failure due to missing credentials -> Completed")

    def test_login_failure_invalid_method(self):
        url = reverse("auth:login")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

        print("Test: Login failure due to invalid method -> Completed")


class UserLogoutViewTestCase(APITestCase):
    def setUp(self):
        self.user = CustomUser.objects.create_superuser(email="testuser@user.com", password="password123")
        self.token = Token.objects.create(user=self.user)

        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

    def test_logout_success(self):
        url = reverse('auth:logout')  # Assuming you have a named URL for the logout view
        headers = {'HTTP_AUTHORIZATION': f'Token {self.token.key}'}
        response = self.client.post(url, **headers)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, {'success': 'Logged out successfully'})

        print("Test: Logout successful -> Completed")

    def test_logout_failure_invalid_token(self):
        url = reverse('auth:logout')  # Assuming you have a named URL for the logout view
        invalid_token_key = 'invalid_token_key'
        headers = {'HTTP_AUTHORIZATION': f'Token {invalid_token_key}'}
        response = self.client.post(url, **headers)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertIn('error', response.data)

        print("Test: Logout failed due to invalid token -> Completed")
