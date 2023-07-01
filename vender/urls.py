from django.urls import path
from vender import views
app_name = "vender"

urlpatterns = [
    
    path('',views.VenderHome.as_view(),name="venderview"),
    path('addcat/',views.AddCategory.as_view(),name="category"),
    path('addfood/',views.AddFood.as_view(),name="food"),
    # path('addrestro/',views.AddRestaurant.as_view(),name="restro"),
    path('FooddeleteView/<int:pk>/',views.FooddeleteView.as_view(),name="deletefood"),
]