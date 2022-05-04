from django.urls import path
from alluser import views
app_name = "alluser"

urlpatterns = [
    path('signup/',views.Signup.as_view(),name="signup"),
    path('login/',views.LoginView.as_view(),name="login"),
    
]