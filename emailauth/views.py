# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import hashlib
import os
import re
from django.shortcuts import render
from django.http import HttpResponse
from django.core.mail import EmailMessage

# Create your views here.


def emailAuthPage(render):
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


def activateUser(request):
    '''Function activates a user, upon usage of link sent to user email.
    '''


def makeUserAuthLink(usr_email):
    '''Function generates a sha256 version of the given email.given

    Will be used as the url/authentication key for a given user.
    '''
    cwd = os.getcwd()
    auth_url = 'hhhippo.tk/emailauth/activate/'
    test_url = '10.10.10.102:8000/emailauth/activate/'

    # check whether in staging, prod, or testing branch
    if re.search(r'.*staging.*', cwd) is None:
        auth_url = 'test.' + auth_url
    elif re.search(r'.*production.*', cwd) is None:
        # do nothing
        pass
    else:
        auth_url = test_url

    sha256_hash = hashlib.sha256()
    sha256_hash.update(usr_email)
    hash_key = sha256_hash.hexdigest()

    auth_url += hash_key

    return auth_url