from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password
from django.core import exceptions

class CreateUserForm(forms.Form):

    user_name = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control','placeholder':'Username'}), max_length=20)
    email = forms.EmailField(widget=forms.TextInput(attrs={'class':'form-control','placeholder':'Email'}), max_length=50)
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class':'form-control','placeholder':'Password'}), max_length=20)
    password_verify = forms.CharField(widget=forms.PasswordInput(attrs={'class':'form-control','placeholder':'Verify Password'}), max_length=20)

    def is_valid(self):
        valid = super(CreateUserForm, self).is_valid()
        if not valid:
            return valid

        user_name = self.cleaned_data['user_name']
        email = self.cleaned_data['email']
        password = self.cleaned_data['password']
        password_verify = self.cleaned_data['password_verify']

        try:
            validate_password(password, user_name)
        except exceptions.ValidationError as e:
            for error in e.messages:
                self.add_error('password', error)
            valid = False
        
        if(password != password_verify):
            self.add_error('password_verify', 'Passwords did not match.')
            valid = False

        if(User.objects.filter(username__iexact=user_name)):
            self.add_error('user_name', 'That user already exists!')
            valid = False

        if(User.objects.filter(email__iexact=email)):
            self.add_error('email', 'That email is already being used.')
            valid = False

        return valid

class LoginForm(forms.Form):
    user_name = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control','placeholder':'Username'}), max_length=20)
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class':'form-control','placeholder':'Password'}), max_length=20)

