from django import forms

class CreateUserForm(forms.Form):
    user_name = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control','placeholder':'Username'}), max_length=20)
    email = forms.EmailField(widget=forms.TextInput(attrs={'class':'form-control','placeholder':'Email'}), max_length=50)
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class':'form-control','placeholder':'Password'}), max_length=20)
    password_verify = forms.CharField(widget=forms.PasswordInput(attrs={'class':'form-control','placeholder':'Verify Password'}), max_length=20)

class LoginForm(forms.Form):
    user_name = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control','placeholder':'Username'}), max_length=20)
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class':'form-control','placeholder':'Password'}), max_length=20)
