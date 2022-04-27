from sre_constants import SUCCESS
from urllib.robotparser import RequestRate
from django.views.generic.edit import CreateView
import datetime
from http import client
from inspect import signature
from multiprocessing import context
import re
from unicodedata import category
from urllib import request
from django.http import HttpResponse
from django.shortcuts import render, redirect
from mainapp.models import Food, Wishlist, Order, Orderline, ShippingAddress, ProductReview
from django.views import View
from django.views.generic.list import ListView
from vender .forms import foodform, Category
from customer.forms import AddressForm, Reviewform
from cart.cart import Cart
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView

from django. db. models import Q
from django.contrib.auth.models import User
from django.views.generic.edit import DeleteView
from django.core.paginator import Paginator
from BestBites import settings
from django.views.decorators.csrf import csrf_exempt
from django.contrib.sites.shortcuts import get_current_site
import razorpay
razorpay_client = razorpay.Client(
    auth=(settings.razorpay_id, settings.razorpay_account_id))

# Create your views here.


class CustomerView(View):
    def get(self, request):
        categories = Category.objects.all()
        foods = Food.objects.all().order_by('name')
        cat = request.GET.get('category')
        if cat:
            foods = foods.filter(category=cat)
        paginator = Paginator(foods, 6)
        page_number = request.GET.get('page')
        pagehere = paginator.get_page(page_number)
        return render(request, "foodie.html", {'categories': categories, 'foods': pagehere})


def cart_add(request, pk):
    cart = Cart(request)
    product = Food.objects.get(pk=pk)
    cart.add(product=product)
    return redirect("/customer/")


def item_clear(request, pk):
    cart = Cart(request)
    product = Food.objects.get(id=pk)
    cart.remove(product)
    return redirect("/customer/cart-detail/")


def item_increment(request, pk):
    cart = Cart(request)
    product = Food.objects.get(id=pk)
    cart.add(product=product)
    return redirect("/customer/cart-detail/")


def item_decrement(request,pk):
    cart = Cart(request)
    # import pdb;pdb.set_trace()
    product = Food.objects.get(pk=pk)
    z = cart.cart.get(str(product.pk))
    if z.get('quantity') == 1:
        item_clear(request, pk)
    else:
        cart.decrement(product=product)
    return redirect("/customer/cart-detail/")


def cart_clear(request):
    cart = Cart(request)
    cart.clear()
    return redirect("/customer/cart-detail/")


def cart_detail(request):
    form = AddressForm()
    return render(request, 'cart_detail.html', {'form': form})


class SearchView(ListView):
    model = Food
    template_name = "searchbar.html"
    context_object_name = "searchbar"

    def get_queryset(self):
        query = self.request.GET.get('q')
        foods = Food.objects.all()
        if query:
            foods = foods.filter(Q(name__icontains=query) | Q(
                restaurants__restorant_name__icontains=query) | Q(category__cat_name__icontains=query))
        return foods


class Mywishlist(ListView):
    model = Wishlist
    template_name = "wishlist.html"
    context_object_name = "wish"


class AddInWishlist(View):
    def get(self, request):
        foodId = request.GET.get('food')
        user = request.user
        food = Food.objects.get(id=foodId)
        food_in_wish = Wishlist.objects.filter(
            Q(food=food) & Q(user=user)).exists()

        if food_in_wish == False:
            Wishlist.objects.create(user=user, food=food)
        return redirect('/customer/')


class Fooddelete(DeleteView):
    model = Wishlist
    template_name = "deleteefood.html"
    success_url = "/customer/"


def payment(request):
    # import pdb; pdb.set_trace()

    if request.method == "POST":
        form = AddressForm(request.POST)
        if form.is_valid():
            form.instance.user = request.user
            form.save()

        address = form.instance
        cart = Cart(request)
        # user =self.request.user
        order = Order.objects.create(
            user=request.user, order_date=datetime.datetime.now(), totalprice=0)
        final_price = 0

        for value in cart.cart.values():
            price = int(value.get('price'))
            quantity = int(value.get('quantity'))
            food = int(value.get('product_id'))
            final_price = final_price + (price*quantity)
            orderline = Orderline.objects.create(
                order=order, totalquantity=quantity, food_id=food)

        order.totalprice = final_price
        callback_url = 'http://' + \
            str(get_current_site(request))+"/customer/handlerequest/"
        print(callback_url)
        razorpay_order = razorpay_client.order.create(dict(
            amount=final_price*100, currency=settings.order_currency, payment_capture='0'))
        print(razorpay_order['id'])
        order.order_id = razorpay_order['id']
        order.save()
        orderline = Orderline.objects.filter(order=order)
        cart.clear()
        return render(request, "paymentmode.html", {'order': order, 'orderline': orderline, 'address': address, 'order_id': razorpay_order['id'], 'final_price': final_price, 'razorpay_merchant_id': settings.razorpay_id, 'callback_url': callback_url})
    else:
        return HttpResponse("505 Not Found")


@csrf_exempt
def handlerequest(request):
    if request.method == "POST":
        order_id = request.POST.get('razorpay_order_id')
        payment_id = request.POST.get('razorpay_payment_id')
        signature = request.POST.get('razorpay_signature')

        params_dict = {
            'razorpay_order_id': order_id,
            'razorpay_payment_id': payment_id,
            'razorpay_signature': signature
        }
        myorder = Order.objects.get(order_id=order_id)
        print(myorder)

        try:
            check = razorpay_client.utility.verify_payment_signature(
                params_dict)
            myorder.status = 'Done'
            myorder.save()
            return render(request, 'success.html')
        except:
            myorder.status = 'Fail'
            myorder.save()
            return render(request, 'cancel.html')


class MyOrder(View):
    def get(self, request):
        form = Reviewform()
        orders = Order.objects.filter(user=request.user)
        result = {}
        for order in orders:
            orderlines = Orderline.objects.filter(order=order)
            result[order] = orderlines
        return render(request, 'orders.html', {'result': result, 'form': form})




class ReviewProduct(View):
    def post(self, request, pk):
        form = Reviewform(request.POST)
        if form.is_valid():
            form.instance.user = request.user
            form.instance.foodId_id = pk
            form.save()
        return redirect("/customer/Order/")


class SingleFood(DetailView):
    model = Food
    template_name = "seefood.html"
    context_object_name = "row"


class Filterby(View):
    def get(self, request):
        sorts = request.GET.get('sort')
        if sorts == "LTH":
            filter = Food.objects.all().order_by('price')
        else:
            filter = Food.objects.all().order_by('-price')
        return render(request, 'filter.html',{'filter': filter})
