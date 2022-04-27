from audioop import reverse
import email
from typing_extensions import Self
from django.test import TestCase
from mainapp.models import User, Category, Restaurants, Food
from django.urls import reverse
from PIL import Image
import io
from django.core.files.base import ContentFile
from io import StringIO
from django.core.files import File
from django.core.files.uploadedfile import SimpleUploadedFile

# Create your tests here.


def create_image(storage, filename, size=(100, 100), image_mode='RGB', image_format='PNG'):

    data = io.BytesIO()
    Image.new(image_mode, size).save(data, image_format)
    data.seek(0)
    if not storage:
        return data
    image_file = ContentFile(data.read())
    return storage.save(filename, image_file)


class Category_Test(TestCase):
    def setUp(self):
        myuser = User.objects.create_user(
            email="jagarti@gmail.com", password="12345", mobile="963258741", role="customer")
        myimage = create_image(None, 'fake.png')
        print(myuser)
        avatar_file = SimpleUploadedFile('front.png', myimage.getvalue())

        self.catg = {"user": myuser.pk,
            "cat_name": "chinese",
            "image": avatar_file
        }

    def test_category(self):
        self.client.login(email="jagarti@gmail.com", password="12345")
        response = self.client.post(
            reverse('vender:category'), self.catg, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertRedirects(response, '/vender/')


class FoodView_Test(TestCase):
    def setUp(self):
        myuser = User.objects.create_user(email="jagarti@gmail.com", password="12345", mobile="963258741", role="customer")
        
        restro = Restaurants.objects.create(
            restorant_name="rangeela bhaba", address="agra", user=myuser)
        category = Category.objects.create(
            cat_name="Itallian", image="ghg.png", user=myuser)

        myimage = create_image(None, 'fake.png')
        avatar_file = SimpleUploadedFile('front.png', myimage.getvalue())

        self.foods = {
                "name": "noodles",
                "description": "tastly",
                "price": "62",
                "category": category.pk,
                "restaurants": restro.pk,
                "image": avatar_file,

                }

    def test_food_post(self):
        response = self.client.post(reverse('vender:food'), self.foods, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertRedirects(response, '/vender/')


class FooddeleteView_Test(TestCase):
    def setUp(self):
        myuser = User.objects.create_user(email="jagarti@gmail.com", password="12345",
                      mobile="963258741", role="customer")
        
        restro = Restaurants.objects.create(restorant_name="rangeela bhaba", address="agra",
                    user=myuser)
        
        category = Category.objects.create(cat_name="Itallian", image="ghg.png", user=myuser)

        myimage = create_image(None, 'fake.png')
        avatar_file = SimpleUploadedFile('front.png', myimage.getvalue())

        
        self.foodie = Food.objects.create(name="noodles", description="tastly", price="62", 
        category=category, restaurants=restro, image=avatar_file)

    def test_food_delete(self):
        response = self.client.delete(reverse('vender:deletefood',kwargs={'pk': self.foodie.pk}))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/vender/')
