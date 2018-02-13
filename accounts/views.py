from django.shortcuts import render
from django.http import HttpResponse

def login(request):
    return HttpResponse('This is the login view.')

def register(request):
    return HttpResponse('This is the register view.')
