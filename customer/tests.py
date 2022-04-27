from django.core.paginator import Paginator
from urllib import response
from django.test import TestCase
from django.urls import reverse
from mainapp.models import User, Category, Restaurants, Food, ShippingAddress
from PIL import Image
import io
from django.core.files.base import ContentFile
from io import StringIO
from django.core.files import File
from django.core.files.uploadedfile import SimpleUploadedFile


def create_image(storage, filename, size=(100, 100), image_mode='RGB', image_format='PNG'):

    data = io.BytesIO()
    Image.new(image_mode, size).save(data, image_format)
    data.seek(0)
    if not storage:
        return data
    image_file = ContentFile(data.read())
    return storage.save(filename, image_file)

# Create your tests here.


class Test_Mywishlist(TestCase):
    def setUp(self):
        myuser = User.objects.create_user(email="jagarti@gmail.com", password="12345",
                      mobile="963258741", role="customer")

        restro = Restaurants.objects.create(restorant_name="rangeela bhaba", address="agra",
                    user=myuser)

        category = Category.objects.create(
            cat_name="Itallian", image="ghg.png", user=myuser)

        myimage = create_image(None, 'fake.png')
        avatar_file = SimpleUploadedFile('front.png', myimage.getvalue())

        self.foodie = Food.objects.create(name="noodles", description="tastly", price="62",
        category=category, restaurants=restro, image=avatar_file)

    def test_category(self):
        response = self.client.get(reverse('customer:wish'))
        self.assertEqual(response.status_code, 200)


class Test_Addtocart(TestCase):
    def setUp(self):
        myuser = User.objects.create_user(email="jenny@gmail.com", password="12345", mobile="963258741",
                    role="customer")

        restro = Restaurants.objects.create(
            restorant_name="rangeela bhaba", address="agra", user=myuser)

        category = Category.objects.create(
            cat_name="Itallian", image="ghg.png", user=myuser)

        myimage = create_image(None, 'fake.png')
        avatar_file = SimpleUploadedFile('front.png', myimage.getvalue())

        self.foodie = Food.objects.create(name="noodles", description="tastly", price="62",
        category=category, restaurants=restro, image=avatar_file)

    def test_cart_add(self):
        self.client.login(email="jenny@gmail.com", password="12345")
        response = self.client.post(
            reverse('customer:cart_add', kwargs={'pk': self.foodie.pk}))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/customer/')

    def test_payment(self):
        self.client.login(email="jenny@gmail.com", password="12345")
        response = self.client.post(
            reverse('customer:cart_add', kwargs={'pk': self.foodie.pk}))
        response = self.client.post(reverse('customer:payment'))
        self.assertEqual(response.status_code, 200)

    def test_item_clear(self):
        self.client.login(email="jagarti@gmail.com", password="12345")
        response = self.client.post(
            reverse('customer:item_clear', kwargs={'pk': self.foodie.pk}))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/customer/cart-detail/')

    def test_item_increment(self):
        # self.client.login(email="jagarti@gmail.com", password="12345")
        response = self.client.post(
            reverse('customer:item_increment', kwargs={'pk': self.foodie.pk}))
        print("india:", self.foodie.pk)

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/customer/cart-detail/')

    def test_item_decrement(self):
        # self.client.login(email="jerry@gmail.com", password="12345")
        response = self.client.post(
            reverse('customer:item_increment', kwargs={'pk': self.foodie.pk}))
        response = self.client.post(
            reverse('customer:item_decrement', kwargs={'pk': self.foodie.pk}))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/customer/cart-detail/')

    def test_cart_clear(self):
        response = self.client.post(reverse('customer:cart_clear'))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, "/customer/cart-detail/")


class Test_Cart_detail(TestCase):
    def setUp(self):
        response = self.client.get(reverse('customer:cart_detail'))
        self.assertEqual(response.status_code, 200)


class Test_SearchView(TestCase):
    def setUp(self):
        myuser = User.objects.create_user(email="jenny@gmail.com", password="12345", mobile="963258741",
                    role="customer")

        restro = Restaurants.objects.create(
            restorant_name="rangeela bhaba", address="agra", user=myuser)

        category = Category.objects.create(
            cat_name="Itallian", image="ghg.png", user=myuser)

        myimage = create_image(None, 'fake.png')
        avatar_file = SimpleUploadedFile('front.png', myimage.getvalue())

        self.foodie = Food.objects.create(name="noodles", description="tastly", price="62",
        category=category, restaurants=restro, image=avatar_file)

    def test_search(self):
        # import pdb;pdb.set_trace()
        response = self.client.get(reverse('customer:mysearch')+'?q=ran')
        self.assertEqual(response.status_code, 200)


class Test_AddInWishlist(TestCase):
    def setUp(self):
        myuser = User.objects.create_user(email="jerry@gmail.com", password="12345", mobile="963258741",
                    role="customer")

        restro = Restaurants.objects.create(
            restorant_name="rangeela bhaba", address="agra", user=myuser)

        category = Category.objects.create(
            cat_name="Itallian", image="ghg.png", user=myuser)

        myimage = create_image(None, 'fake.png')
        avatar_file = SimpleUploadedFile('front.png', myimage.getvalue())

        self.foodie = Food.objects.create(name="noodles", description="tastly", price="62",
        category=category, restaurants=restro, image=avatar_file)

    def test_addwishlist(self):
        self.client.login(email="jerry@gmail.com", password="12345")
        response = self.client.get(
            reverse('customer:addinwishlist')+f'?food={self.foodie.pk}')
        self.assertEqual(response.status_code, 302)


class Test_ReviewProduct(TestCase):
    def setUp(self):
        myuser = User.objects.create_user(email="jerry@gmail.com", password="12345", mobile="963258741",
                    role="customer")

        restro = Restaurants.objects.create(
            restorant_name="rangeela bhaba", address="agra", user=myuser)

        category = Category.objects.create(
            cat_name="Itallian", image="ghg.png", user=myuser)

        myimage = create_image(None, 'fake.png')
        avatar_file = SimpleUploadedFile('front.png', myimage.getvalue())

        self.foodie = Food.objects.create(name="noodles", description="tastly", price="62",
        category=category, restaurants=restro, image=avatar_file)

    def test_review(self):
        self.client.login(email="jerry@gmail.com", password="12345")
        response = self.client.post(
            reverse('customer:review', kwargs={'pk': self.foodie.pk}))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, "/customer/Order/")


class Test_Filterby(TestCase):
    def setUp(self):
        myuser = User.objects.create_user(email="jerry@gmail.com", password="12345", mobile="963258741",
                    role="customer")

        restro = Restaurants.objects.create(
            restorant_name="rangeela bhaba", address="agra", user=myuser)

        category = Category.objects.create(
            cat_name="Itallian", image="ghg.png", user=myuser)

        myimage = create_image(None, 'fake.png')
        avatar_file = SimpleUploadedFile('front.png', myimage.getvalue())

        self.foodie = Food.objects.create(name="noodles", description="tastly", price="62",
        category=category, restaurants=restro, image=avatar_file)

    def test_filter(self):
        # import pdb; pdb.set_trace()
        response = self.client.get(reverse('customer:filter')+'?sort=LTH')
        self.assertEqual(response.status_code, 200)


class Test_CustomerView(TestCase):
    def setUp(self):
        myuser = User.objects.create_user(email="jerry@gmail.com", password="12345", mobile="963258741",
                    role="customer")

        restro = Restaurants.objects.create(
            restorant_name="rangeela bhaba", address="agra", user=myuser)

        self.category = Category.objects.create(
            cat_name="Itallian", image="ghg.png", user=myuser)
        self.category1 = Category.objects.create(
            cat_name="indian", image="ghg3.png", user=myuser)

        myimage = create_image(None, 'fake.png')
        avatar_file = SimpleUploadedFile('front.png', myimage.getvalue())

        self.foodie = Food.objects.create(name="noodles", description="tastly", price="62",
        category=self.category, restaurants=restro, image=avatar_file)
        self.foodie1 = Food.objects.create(name="noodles", description="tastly", price="62",
        category=self.category1, restaurants=restro, image=avatar_file)

    def test_view(self):
        # import pdb; pdb.set_trace()
        self.client.login(email="jerry@gmail.com", password="12345")
        response = self.client.get(
            reverse('customer:customerview')+f'?category={self.category.pk}')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed("foodie.html")

    def test_pagination(self):
        self.client.login(email="jerry@gmail.com", password="12345")
        response = self.client.get(reverse('customer:customerview')+'?page=1')
        print("hiii delhi:",response)
        self.assertEqual(response.status_code, 200)

    
   


       



        # class CountContainer:
        #        def count(self):
        #           return 12
       
        #    # Paginator can be passed other objects with a count() method.
        
        # import pdb; pdb.set_trace() 
        # paginator = Paginator(CountContainer(), 6)
        # self.assertEqual(12, paginator.count)
        # self.assertEqual(2, paginator.num_pages)
        # self.assertEqual([1,2], list(paginator.page_range))
        # self.assertEqual(response.status_code, 200)




   
        













