from django.urls import path
from alluser import views

urlpatterns = [
    path('Signup/',views.Signup.as_view()),
    path('LoginView/',views.LoginView.as_view(),name="login"),
    
]