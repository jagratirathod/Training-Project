from django.core.paginator import Paginator
from django.views.generic.edit import DeleteView
from django.views.generic.edit import CreateView
from django.views.generic.list import ListView
from mainapp.models import Category, Food
from django.shortcuts import render, redirect
from.forms import categoryform, foodform


# Create your views here.


class homeView(ListView):
    paginate_by = 6
    model = Food
    context_object_name = "foods"
    template_name = "home1.html"

    def get_context_data(self, **kwargs):
        cat=Category.objects.all()
        context=super().get_context_data(**kwargs)
        context['cat']=cat
        return context

class AddCategory(CreateView):
    model = Category
    form_class = categoryform
    template_name = "addCat.html"
    success_url = "/vender/"

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


class FoodView(CreateView):
    model = Food
    form_class = foodform
    template_name = "foods.html"
    success_url = "/vender/"


class FooddeleteView(DeleteView):
    model = Food
    success_url = "/vender/"
    template_name = "deletefood.html"
