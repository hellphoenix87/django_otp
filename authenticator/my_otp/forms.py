from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User

class LoginForm(AuthenticationForm):
    
    otp_token = forms.CharField(max_length=6, widget=forms.TextInput(attrs={'autocomplete': 'off'}))

    
    class Meta:
        model = User
        fields = ['username', 'password']