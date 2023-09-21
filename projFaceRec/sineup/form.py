# for username,password,confirm password
from django.contrib.auth.forms import UserCreationForm
# for firstname,lastname,email,image,role
from .models import customuser
from django import forms

class customcreatefrom(UserCreationForm):
    password2 = forms.CharField(label='Confirm Password', widget=forms.PasswordInput)   
    class Meta:
        model = customuser
        fields = ["username","first_name","last_name","email","Role","Imege"]
        widgets = {
            'Role': forms.TextInput(attrs={'placeholder': 'Enter your role'}),
        }