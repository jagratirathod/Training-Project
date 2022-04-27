from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.views.generic.edit import CreateView
from mainapp.models import User
from .forms import Signupform, Loginform
from django.contrib.auth import authenticate, login
from django.contrib.messages.views import SuccessMessageMixin


# Create your views here.


class Signup(SuccessMessageMixin, CreateView):
    form_class = Signupform
    template_name = "signup.html"
    success_url = "/alluser/LoginView/"
    success_message = "Successfully Signed ...!"


class LoginView(CreateView):
    # model = User
    # fields = ['email', 'password']
    form_class = Loginform
    template_name = "login.html"
    context_object_name = 'loginhere'
    success_url = "/alluser/Login/"

    def post(self, request):
        email = request.POST.get('email')
        password = request.POST.get('password')

        user = authenticate(email=email, password=password)

        if user:
            login(request, user)
            if user.role == "vender":
                return redirect("/vender/")
            else:
                return redirect('/customer/')
        else:
            return HttpResponse("Invalid user")
