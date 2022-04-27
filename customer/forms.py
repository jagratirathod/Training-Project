from django import forms
from mainapp.models import ShippingAddress, ProductReview
from vender.forms import foodform
# from django_countries.widgets import CountrySelectWidget    


class AddressForm(forms.ModelForm):

    class Meta:
        model = ShippingAddress
        fields = ("street_address", "apartment_address", "country", "zip_code",
                  "city","payment_option")



class Reviewform(forms.ModelForm):
    class Meta:
        model = ProductReview
        fields = ("comment","rating")
