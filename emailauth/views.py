# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.http import HttpResponse
from django.core import mail

# Create your views here.

def index(render):
    return HttpResponse('Sending email...')


def sendEmail():
    '''Function sends an authentication email'''

    emailConfig()

    mail = mail.EmailMessage(
    'Hello',
    'Body goes here',
    'noreply.hhhippo@gmail.com',
    ['connor.runyan@aggiemail.usu.edu'],
    [],
    reply_to=[],
    headers={'Message-ID': 'foo'})
    

def emailConfig():
    mail.settings.EMAIL_HOST_USER = 'noreply.hhhippo@gmail.com'
    mail.settings.EMAIL_HOST_PASSWORD = 'Hungry4evr' 
