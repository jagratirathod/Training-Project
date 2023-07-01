from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView
from BestBites import settings
from mainapp.models import User
from .forms import Signupform, Loginform
from django.contrib.auth import authenticate, login
from django.contrib.messages.views import SuccessMessageMixin
from django.core.mail import send_mail

# Create your views here.


class Signup(SuccessMessageMixin, CreateView):
    form_class = Signupform
    template_name = "signup.html"
    success_url = reverse_lazy('alluser:login')
    success_message = "Successfully Signed ...!"

   
    def form_valid(self,form):
        send_mail(subject="BestBites", message="Your registration has been done successfully",from_email=settings.EMAIL_HOST_USER, recipient_list=[form.instance.email])
        return super().form_valid(form)

class LoginView(CreateView):
    # model = User
    # fields = ['email', 'password']
    form_class = Loginform
    template_name = "login.html"
    context_object_name = 'loginhere'
    success_url = reverse_lazy('alluser:login')

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
