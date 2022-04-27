from django.contrib import admin
from . models import( User,Restaurants,Category,Food,Order,Orderline,Wishlist,
                        ShippingAddress, ProductReview)

# Register your models here.

class UserAdmin(admin.ModelAdmin):
    list_display=['email','first_name','last_name','mobile','role','password']
admin.site.register(User,UserAdmin)


class RestaurantAdmin(admin.ModelAdmin):
    list_display=['id','restorant_name','address','user']
admin.site.register(Restaurants,RestaurantAdmin)

class CategoryAdmin(admin.ModelAdmin):
    list_display=['id','cat_name','image','user']
admin.site.register(Category,CategoryAdmin)

class Foodadmin(admin.ModelAdmin):
    list_display=['id','name','description','price','image','category','restaurants']
admin.site.register(Food,Foodadmin)

class OrderAdmin(admin.ModelAdmin):
    list_display=['id','user','totalprice','order_date','status','order_id']
admin.site.register(Order,OrderAdmin)

class OrderlineAdmin(admin.ModelAdmin):
    list_display=['id','totalquantity','food','order']
admin.site.register(Orderline,OrderlineAdmin)

class WishlistAdmin(admin.ModelAdmin):
    list_display=['user','food']
admin.site.register(Wishlist,WishlistAdmin)

class ShippingAddressAdmin(admin.ModelAdmin):
    list_display=['street_address','apartment_address','country','zip_code']
admin.site.register(ShippingAddress,ShippingAddressAdmin)

class ReviewsAdmin(admin.ModelAdmin):
     list_display=['user','foodId','comment','rating']
admin.site.register(ProductReview,ReviewsAdmin)
