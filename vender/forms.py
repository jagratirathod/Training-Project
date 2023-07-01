from django import forms
from mainapp.models import Category,Food


class categoryform(forms.ModelForm):
    
    class Meta:
        model = Category
        fields = ("cat_name","image",)


class foodform(forms.ModelForm):
    
    class Meta:
        model = Food
        fields = ("name","description","price","image","category","restaurant")


# class Restaurantform(forms.ModelForm):
    
#     class Meta:
#         model = Restaurants
#         fields = ('restorant_name','address','user')