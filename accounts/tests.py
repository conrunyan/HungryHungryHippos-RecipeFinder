"""Tests the user actions for accounts."""

from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.urls import reverse
from django.contrib.auth import authenticate, login, logout, get_user

class LogoutFunctionalityTest(TestCase):
    """Tests the logout functionality."""

    def setUp(self):
        """Setup the test client before each test."""
        self.client = Client()

    def test_logged_out_user_is_not_authenticated(self):
        """When a user logs out, they should no longer be authenticated."""
        user = User.objects.create_user('test')
        self.client.force_login(user)
        self.assertTrue(get_user(self.client).is_authenticated())
        self.client.get(reverse('logout'))
        self.assertFalse(get_user(self.client).is_authenticated())

    def test_logging_out_user_returns_good_status_code(self):
        """When a user logs out, the response should return a good status code."""
        response = self.client.get(reverse('logout'))
        self.assertEqual(response.status_code, 302)


class LoginFunctionalityTest(TestCase):
    """Tests the login functionality."""

    def setUp(self):
        """Setup the test client before each test."""
        self.client = Client()

    def test_user_is_authenticated_once_logged_in(self):
        """Once a user is successfully logged in, they should be authenticated."""
        user = User.objects.create_user(username='test', password='password')
        self.assertFalse(get_user(self.client).is_authenticated())
        self.client.login(username="test",password="password")
        self.assertTrue(get_user(self.client).is_authenticated())

    def test_cannot_log_in_if_username_is_incorrect(self):
        """A user should not be able to log in if they input an invalid username."""
        user2 = User.objects.create_user(username='test2', password='password')
        self.client.login(username="",password="password")
        self.assertFalse(get_user(self.client).is_authenticated())

    def test_cannot_log_in_if_password_is_incorrect(self):
        """A user should not be able to log in if they input an invalid password."""
        user3 = User.objects.create_user(username='test3', password='password')
        self.client.login(username="test3",password="")
        self.assertFalse(get_user(self.client).is_authenticated())

    def test_logging_in_user_returns_good_status_code(self):
        """When a user logs in, the response should return a good status code."""
        user4= User.objects.create_user(username='test4', password='password')
        response = self.client.post(reverse('login'),{ 'user_name' : 'test4', 'password' : 'password' })
        self.assertEqual(response.status_code, 302)
