from django import forms
from django.contrib.auth.models import User


class UserLogin(forms.Form):
    username = forms.CharField(max_length=100)
    password = forms.CharField(widget=forms.PasswordInput)

class SendMessage(forms.Form):
    body = forms.CharField(widget=forms.Textarea,
                           label='Enter your message')