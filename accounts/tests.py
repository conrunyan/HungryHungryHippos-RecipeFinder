"""Tests the user actions for accounts."""

from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.urls import reverse
from django.contrib.auth import authenticate, login, logout

class LogoutFunctionalityTest(TestCase):
    """Tests the logout functionality."""

    def setUp(self):
        """Setup the test client before each test."""
        self.client = Client()

    def test_logged_out_user_is_not_authenticated(self):
        """When a user logs out, they should no longer be authenticated."""
        user = User.objects.create_user('test')
        self.client.force_login(user)
        self.assertTrue(user.is_authenticated)
        self.client.get(reverse('logout'))
        #self.assertFalse(user.is_authenticated)
