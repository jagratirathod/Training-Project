from django.urls import path
from customer import views

app_name = "customer"
urlpatterns = [
    path('', views.CustomerView.as_view(), name="customerview"),
    path('Filterby/', views.Filterby.as_view(),name="filter"),
    path('ReviewProduct/<int:pk>/', views.ReviewProduct.as_view(),name="review"),
    path('SingleFood/<int:pk>/', views.SingleFood.as_view(),name='singlefood'),
    path('payment/', views.payment,name="payment"),
    path('Order/', views.MyOrder.as_view()),
    path('Mywishlist/', views.Mywishlist.as_view(), name="wish"),
    path('Fooddelete/<int:pk>/', views.Fooddelete.as_view(), name="delete"),
    path('AddInWishlist/', views.AddInWishlist.as_view(),name="addinwishlist"),
    path('SearchView/', views.SearchView.as_view(), name='mysearch'),
    path('cart_add/<int:pk>/', views.cart_add, name='cart_add'),
    path('item_clear/<int:pk>/', views.item_clear, name='item_clear'),
    path('item_increment/<int:pk>/', views.item_increment, name='item_increment'),
    path('item_decrement/<int:pk>/', views.item_decrement, name='item_decrement'),
    path('cart_clear/', views.cart_clear, name='cart_clear'),
    path('cart-detail/', views.cart_detail, name='cart_detail'),
    path('handlerequest/', views.handlerequest, name='handlerequest'),

]
