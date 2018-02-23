from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout

from .forms import CreateUserForm, LoginForm

def login_view(request):
	if request.method == 'POST':
		form = LoginForm(request.POST)

		if form.is_valid():
			user_name = form.cleaned_data['user_name']
			password = form.cleaned_data['password']

			user = authenticate(request, username=user_name, password=password)
			if user is not None:
				login(request, user)
				return redirect('recipe:index')
			else:
				form.add_error(None, 'Invalid Username/Password')

	else:
		form = LoginForm()

	context = {'form' : form}
	return HttpResponse(render(request, 'accounts/login.html', context))

def register_view(request):
	if request.method == 'POST':
		form = CreateUserForm(request.POST)

		if form.is_valid():
			user_name = form.cleaned_data['user_name']
			email = form.cleaned_data['email']
			password = form.cleaned_data['password']
			password_verify = form.cleaned_data['password_verify']

			if(password != password_verify):
				form.add_error('password_verify', 'Passwords did not match')

			if(User.objects.filter(username=user_name)):
				form.add_error('user_name', 'That user already exists!')

			if(form.is_valid()):
				User.objects.create_user(user_name, email, password)
				success_context = { 'user_name' : user_name, 'email' : email}
				user = authenticate(request, username=user_name, password=password)
				if user is not None:
					login(request, user)
				else:
					form.add_error(None, 'Failed to create account')
					context = {'form' : form}
					return HttpResponse(render(request, 'accounts/register.html', context))
				return render(request, 'accounts/register_successful.html', success_context)

	else:
		form = CreateUserForm()

	context = {'form' : form}
	return HttpResponse(render(request, 'accounts/register.html', context))

def logout_view(request):
	logout(request)
	response = redirect('recipe:index')
	response.user = request.user
	return response
