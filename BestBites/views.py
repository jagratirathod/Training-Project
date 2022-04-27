from django.shortcuts import render
from django.views.generic.list import ListView
from mainapp .models import Category,Food

# from alluser import models



class Home(ListView):
    def get(self, request):
        return render(request, "home.html")




    





