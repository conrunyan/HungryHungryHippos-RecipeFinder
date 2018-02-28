# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import pdb
import hashlib
from django.test import TestCase
from .models import EmailAuth, makeUserAuthLink, makeEmailAuth
from django.contrib.auth.models import User
from .views import sendAuthEmail, activateUser

# Create your tests here.

class TestViews(TestCase):
	'''Suite of tests to make sure key views methods work as expected'''
	def setUp(self):
		user = User.objects.create_user('test1', 'test1@test.com', 'password')
		EmailAuth.objects.create(usr_id=user, is_authenticated=False, authentication_id='HASHED KEY')


	def test_activateUser(self):
		user = User.objects.get(email='test1@test.com')
		auth_usr = EmailAuth.objects.get(usr_id=user)
		auth_id = auth_usr.authentication_id
		cur_usr = activateUser(auth_id)
		self.assertEqual(cur_usr.is_authenticated, True)


	def test_sendAuthEmail(self):
		email = sendAuthEmail('connor.runyan@aggiemail.usu.edu')
		self.assertEqual(email, 'connor.runyan@aggiemail.usu.edu')


class TestModels(TestCase):
	'''Suite of tests to make sure key elements in the models are working'''
	def setUp(self):
		user = User.objects.create_user('test1', 'test1@test.com', 'password')
		EmailAuth.objects.create(usr_id=user, is_authenticated=False, authentication_id='HASHED KEY')


	def test_makeAuthLink(self):
		email = 'connor.runyan@aggiemail.usu.edu'
		hashed_email = hashlib.sha256()
		hashed_email.update(email)
		hashed_email = hashed_email.hexdigest()
		link = 'localhost:8000/emailauth/activate/?auth=' + hashed_email
		func_hash = makeUserAuthLink(email)
		self.assertEqual(link, func_hash)


	def test_makeEmailAuth(self):
		user = User.objects.get(email='test1@test.com')











