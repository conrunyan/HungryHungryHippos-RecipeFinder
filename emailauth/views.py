# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.http import HttpResponse
from django.core.mail import EmailMessage

# Create your views here.

def index(render):
    return HttpResponse('Sending email...')


def sendEmail():
    '''Function sends an authentication email'''

    my_mail = EmailMessage(
    'Hello',
    'Body goes here',
    'noreply.hhhippo@gmail.com',
    ['connor.runyan@aggiemail.usu.edu'],
    [],
    reply_to=[],
    headers={'Message-ID': 'foo'})

    my_mail.send()
