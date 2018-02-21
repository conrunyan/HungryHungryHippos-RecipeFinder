from django import forms

class CreateUserForm(forms.Form):
    user_name = forms.CharField(label='User Name', max_length=20)
    email = forms.EmailField(label='Email')
    password = forms.CharField(widget=forms.PasswordInput(), label='Password', max_length=20)
    password_verify = forms.CharField(widget=forms.PasswordInput(), label='Password Verify', max_length=20)
