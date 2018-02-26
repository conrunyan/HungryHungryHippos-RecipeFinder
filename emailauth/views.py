# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import hashlib
import os
import re
from django.shortcuts import render
from django.http import HttpResponse
from django.core.mail import EmailMessage
from .models import EmailAuth

# Create your views here.


def emailAuthPage(request):
    if request.method == 'GET':
        auth_id = request.GET['id']
        activateUser(auth_id)
        return HttpResponse('Your account has been successfully activated! Thanks for joining!')


def sendAuthEmail(email_addr):
    '''Function sends an authentication email to the email passed as an argument.
    '''
    auth_link = makeUserAuthLink(email_addr)

    subj = 'Hungry Hungry Hippos Email Authentication'
    body = 'Hello!\n\n\
Thank you for signing up with us!\n\
Before you can add your own recipes, you will need to authenticate your email.\n\
Please click the link below to activate your account, and get started on your epic cooking journey!\n\n\
{0} \n\n\
NOTE: DO NOT REPLY TO THESE EMAILS. IF YOU WISH TO CONTACT US, SEND AN EMAIL TO (some.email...) OR CALL US AT (some number)\n'.format(auth_link)
    from_email = 'noreply.hhhippo@gmail.com'
    to_email = [email_addr]
    bcc = []

    auth_mail = EmailMessage(subj, body, from_email, to_email, bcc, reply_to=[], headers={'Message-ID': 'foo'})
    auth_mail.send()

    return to_email[0]


def validateEmail(email_addr):
    '''Function checks if an email address is valid. Returns true if yes, false if not.
    '''
    # may not need to do this. If there's time, go for it...
    pass


def activateUser(auth_id):
    '''Function activates a user, upon usage of link sent to user email.
    '''
    # had to do it this way because python = dumb
    cur_usr = EmailAuth.objects.get(authetication_id=auth_id)
    cur_usr.is_auth = True
    cur_usr.save()
