# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import hashlib
from django.shortcuts import render
from django.http import HttpResponse
from django.core.mail import EmailMessage
from django.contrib.auth.models import User

# Create your views here.


def emailAuthPage(render):
    to_email = sendAuthEmail()
    return HttpResponse('An email authentication has been sent to: {0}'.format(to_email))


def sendAuthEmail(usr_email):
    '''Function sends an authentication email to the email passed as an argument.
    '''
    subj = 'Hello'
    body = 'This is an email body'
    from_email = 'noreply.hhhippo@gmail.com'
    to_email = list(usr_email)
    bcc = []

    auth_mail = EmailMessage(subj, body, from_email, to_email, bcc, reply_to=[], headers={'Message-ID': 'foo'})

    auth_mail.send()

    return to_email[0]


def validateEmail(email_addr):
    '''Function checks if an email address is valid. Returns true if yes, false if not.
    '''
    # may not need to do this. If there's time, go for it...
    pass


def activateUser(request):
    '''Function activates a user, upon usage of link sent to user email.
    '''


def getUserAuthKey(user_id):
    '''Call to User database to find user's email and key'''
    user = User.objects.get(id=user_id)
    print user.email

    
