from django.test import TestCase, Client
from django.urls import reverse


# Create your tests here.
class TestAuth(TestCase):
    def setUp(self) -> None:
        self.client = Client()

    def test_user_register(self):
        payload = {
            'phone_number': '01752495467',
            'name': 'saifullah',
            'password': '123456',
        }
        response = self.client.post(reverse('auth:register'), payload, format="json")
        self.assertEquals(response.json()['phone_number'], '01752495467')
        self.assertEquals(response.status_code, 201)

    # def test_user_login(self):
    #     payload = {
    #         'phone_number': '01752495467',
    #         'password': '123456',
    #     }
    #     response = self.client.post(reverse('auth:login'), payload, format="json")
    #     print(response.json())
    #     self.assertEquals(response.status_code, 201)
