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

    def dump(self, obj):
        for attr in dir(obj):
            try:
                print("obj.%s = %r" % (attr, getattr(obj, attr)))
            except AttributeError:
                print("Error getting attribute")

    def test_logged_out_user_is_not_authenticated(self):
        """When a user logs out, they should no longer be authenticated."""
        user = User.objects.create_user('test')
        self.client.force_login(user)
        self.assertTrue(user.is_authenticated())
        response = self.client.get(reverse('logout'))
        self.assertFalse(response.user.is_authenticated())
