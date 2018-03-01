"""Tests the user actions for accounts."""

from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.urls import reverse
from django.contrib.auth import authenticate, login, logout, get_user

from accounts.forms import CreateUserForm

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

class CreateUserFormTest(TestCase):
    """ Tests CreateUserForm """

    def test_vaild(self):
        '''Form is valid'''
        form = CreateUserForm(data={
            'user_name':       'test',
            'email':           'test@test.com',
            'password':        '!@HesJwir3442@',
            'password_verify': '!@HesJwir3442@'
            })
        self.assertTrue(form.is_valid())

    def test_invalid_mismatch_passwords(self):
        '''When passwords don't match, form is invalid and throws error message'''
        form = CreateUserForm(data={
            'user_name':       'test',
            'email':           'test@test.com',
            'password':        '!@HesJwir3442@',
            'password_verify': 'BLLLLEEEERRRG!!!'
            })
        self.assertFalse(form.is_valid())
        self.assertEqual(form['password_verify'].errors[0], "Passwords did not match.")

    def test_invalid_duplicate_user(self):
        '''When user already exists(case insensitive), form is invalid and throws error message'''
        User.objects.create_user('TeSt','pass')
        form = CreateUserForm(data={
            'user_name':       'tEsT',
            'email':           'test@test.com',
            'password':        '!@HesJwir3442@',
            'password_verify': '!@HesJwir3442@'
            })
        self.assertFalse(form.is_valid())
        self.assertEqual(form['user_name'].errors[0], "That user already exists!")

    def test_invalid_duplicate_email(self):
        '''When email is duplicated from another account, form is invalid and throws error message'''
        User.objects.create_user('tester','test@test.com','pass')
        form = CreateUserForm(data={
            'user_name':       'test',
            'email':           'test@test.com',
            'password':        '!@HesJwir3442@',
            'password_verify': '!@HesJwir3442@'
            })
        self.assertFalse(form.is_valid())
        self.assertEqual(form['email'].errors[0], "That email is already being used.")

    def test_invalid_django_validation(self):
        '''When passwords don't pass django validation, form is invalid and throws error message'''
        form = CreateUserForm(data={
            'user_name':       'test',
            'email':           'test@test.com',
            'password':        'password', #common password -- should fail
            'password_verify': 'password'
            })
        self.assertFalse(form.is_valid())
        self.assertEqual(form['password'].errors[0], "This password is too common.")  

    def test_invalid_incomplete(self):
        '''When form isn't completely filled out, form is not valid'''
        form = CreateUserForm(data={
            'user_name':       'test',
            'password':        '!@HesJwir3442@',
            'password_verify': '!@HesJwir3442@'
            })
        self.assertFalse(form.is_valid())

class CreateUserViewTest(TestCase):

    def setUp(self):
        """Setup the test client before each test."""
        self.client = Client()

    def test_successful_creation(self):
        response = self.client.post(reverse('register'), {
            'user_name' : 'test',
            'email' : 'email@email.com',
            'password' : 'This is a strong p',
            'password_verify' : 'This is a strong p'
            })
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Account Created Sucessfully')
        self.assertEqual(User.objects.get(username='test').username,'test')

    def test_missing_form_field_creation(self):
        response = self.client.post(reverse('register'), {
            'email' : 'email@email.com',
            'password' : 'This is a strong p',
            'password_verify' : 'This is a strong p'
            })
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'This field is required.')
        self.assertRaises(User.DoesNotExist, User.objects.get, username='test')

    def test_form_errors(self):
        User.objects.create_user('test','test@test.com','pass')
        response = self.client.post(reverse('register'), {
            'user_name' : 'test',
            'email' : 'test@test.com',
            'password' : 'password',
            'password_verify' : 'Blahblerg'
            })
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'That user already exists!')
        self.assertContains(response, 'That email is already being used.')
        self.assertContains(response, 'Passwords did not match.')
        self.assertContains(response, 'This password is too common.')
