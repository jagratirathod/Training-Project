from calendar import c
from django import forms
from django.contrib.auth.forms import UserCreationForm
from mainapp.models import User

class Signupform(UserCreationForm):

    class Meta:
        model = User
        fields = ("email","password1","password2","first_name","last_name","role","mobile")
    

class Loginform(forms.ModelForm):
    
    class Meta:
        model = User
        fields = ("email","password",)




