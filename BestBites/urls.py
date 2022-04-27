from django.conf import settings
from django.contrib import admin
from django.urls import path,include
from BestBites import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',views.Home.as_view()),
    path('alluser/',include('alluser.urls')),
    path('vender/',include('vender.urls')),
    path('customer/',include('customer.urls'))


]+static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
