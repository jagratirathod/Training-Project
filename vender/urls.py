from django.urls import path
from vender import views
app_name = "vender"

urlpatterns = [
    
    path('',views.homeView.as_view(),name="vender"),
    path('addcat/',views.AddCategory.as_view(),name="category"),
    path('FoodView/',views.FoodView.as_view(),name="food"),
    path('FooddeleteView/<int:pk>/',views.FooddeleteView.as_view(),name="deletefood"),
]