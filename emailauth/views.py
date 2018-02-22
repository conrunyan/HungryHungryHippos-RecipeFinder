# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.http import HttpResponse
from django.core.mail import EmailMessage

# Create your views here.

def emailAuthPage(render):
    to_email = sendEmail()
    return HttpResponse('An email authentication has been sent to: {0}'.format(to_email))


def sendEmail():
    '''Function sends an authentication email.
    '''
    subj = 'Hello'
    body = 'This is an email body'
    from_email = 'noreply.hhhippo@gmail.com'
    to_email = ['connor.runyan@aggiemail.usu.edu']
    bcc = []

    my_mail = EmailMessage(subj, body, from_email, to_email, bcc, reply_to=[], headers={'Message-ID': 'foo'})

    my_mail.send()

    return to_email[0]

def validateEmail(email_addr):
    '''Function checks if an email address is valid. Returns true if yes, false if not.
    '''


def activateUser():
    '''Function activates a user, upon usage of link sent to user email.
    '''
