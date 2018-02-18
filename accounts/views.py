from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.models import User

from .forms import CreateUserForm

def login(request):
	context = { }
	return HttpResponse(render(request, 'accounts/login.html', context))

def register(request):
	if request.method == 'POST':
		message = ""
		form = CreateUserForm(request.POST)
		if form.is_valid():
			if(form.cleaned_data['password'] == form.cleaned_data['password_verify']):
				user = User.objects.create_user(form.cleaned_data['user_name'], form.cleaned_data['email'], form.cleaned_data['password'])
				message = 'Account creaded successfully'
			else:
				message = request, 'Passwords did not match'
			return HttpResponse(message)
	else: 
		form = CreateUserForm();
	
	context = {'form' : form}
	return HttpResponse(render(request, 'accounts/register.html', context))

def logout(request):
	context = { }
	return HttpResponse(render(request, 'accounts/logout.html', context))
