from django.test import TestCase
from mainapp. models import User

# Create your tests here.


class LogIn_Test(TestCase):
    def setUp(self):
        self.data1 = {
            'email': 'vender@gmail.com',
            'password': '12345',
            'role': 'vender'
        }

        self.data2 = {
            'email': 'customer@gmail.com',
            'password': '12345',
            'role': 'customer',
        }

        User.objects.create_user(**self.data1)
        User.objects.create_user(**self.data2)

        # print(User.objects.all())
        # print("hiii:",x,y)
        
    def test_vender(self):
        response = self.client.post('/alluser/LoginView/', self.data1, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertRedirects(response, '/vender/')

    def test_customer(self):
        response = self.client.post('/alluser/LoginView/', self.data2, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertRedirects(response, '/customer/')
