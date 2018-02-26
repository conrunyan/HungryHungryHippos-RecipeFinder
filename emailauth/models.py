# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User
from .views import makeUserAuthLink


class EmailAuth(models.Model):
    '''Class contains email user authentication status'''

    usr_id = models.ForeignKey(User, on_delete=models.CASCADE)
    is_authenticated = models.BooleanField()
    authentication_id = models.CharField(max_length=10000)

    def __str__(self):
        '''Returns a string with the email and authentication flag values'''
        return 'Email: {0} Authentication Status: {1}'.format(self.authentication_id, self.is_authenticated)


def makeEmailAuth(user, is_auth):
    email = user.email
    auth_id = makeUserAuthLink(email)
    EmailAuth.objects.create(usr_id=user, is_authenticated=False, authentication_id=auth_id)
    ea = EmailAuth.objects.get(usr_id=user)
    print('Email Auth model created', str(ea))
