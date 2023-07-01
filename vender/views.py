from unicodedata import category
from django.core.paginator import Paginator
from django.views import View
from django.views.generic.edit import DeleteView
from django.views.generic.edit import CreateView
from django.views.generic.list import ListView
from requests import request
from mainapp.models import Category, Food
from django.shortcuts import render, redirect
from.forms import categoryform, foodform
from django.urls import reverse_lazy


# Create your views here.


class VenderHome(View):
    def get(self,request):
        cat=Category.objects.all()
        foods = Food.objects.filter(user=request.user)
        print(foods)
        return render(request,"venderhome.html",{'cat':cat,'foods':foods})
        

class AddCategory(CreateView):
    model = Category
    form_class = categoryform
    template_name = "addCat.html"
    success_url = reverse_lazy("vender:venderview")

    def form_valid(self,form):
        form.instance.user = self.request.user
        return super().form_valid(form)


class AddFood(CreateView):
    model = Food
    form_class = foodform
    template_name = "foods.html"
    success_url = reverse_lazy("vender:venderview")

    def form_valid(self,form):
        form.instance.user = self.request.user
        return super().form_valid(form)

# class AddRestaurant(CreateView):
#     model = Restaurants
#     form_class = Restaurantform
#     template_name = "restro.html"
#     success_url = reverse_lazy("vender:venderview")


class FooddeleteView(DeleteView):
    model = Food
    success_url = reverse_lazy("vender:venderview")
    template_name = "deletefood.html"
