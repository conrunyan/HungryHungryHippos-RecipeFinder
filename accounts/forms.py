from django import forms
from django.contrib.auth.models import User

class CreateUserForm(forms.Form):
	user_name = forms.CharField(label='User Name', max_length=20)
	email = forms.EmailField(label='Email')
	password = forms.CharField(widget=forms.PasswordInput(), label='Password', max_length=20)
	password_verify = forms.CharField(widget=forms.PasswordInput(), label='Password Verify', max_length=20)

	def is_valid(self):
		valid = super(CreateUserForm, self).is_valid()
		if not valid:
			return valid

		user_name = self.cleaned_data['user_name']
		email = self.cleaned_data['email']
		password = self.cleaned_data['password']
		password_verify = self.cleaned_data['password_verify']

		if(len(password) < 6):
			self.add_error('password', 'Password must contain at least 6 characters')
			valid = False
		
		if(password != password_verify):
			self.add_error('password_verify', 'Passwords did not match')
			valid = False

		if(User.objects.filter(username=user_name)):
			self.add_error('user_name', 'That user already exists!')
			valid = False

		return valid