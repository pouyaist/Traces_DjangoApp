from django.test import TestCase
from user.factories import UserProfileFactory, UserAuthFactory
from django.test.client import Client, RequestFactory

class TestRegister(TestCase):
    def setUp(self):
        self.user_auth = UserAuthFactory(username="user", password="pass", email="user@gmail.com")
        self.user_auth.save()
        self.user = UserProfileFactory(user_auth = self.user_auth, phone = '0123456789', city = 'Eind')
        self.user.save()
        self.client = Client()
        self.factory = RequestFactory()

    def test_register_valid_user(self):
        data={
            'username': 'dima',
            'password': '123123',
            'email': 'Hi@there.com',
            'first_name': 'dima',
            'last_name': 'k',
            'city': 'Kiev',
            'phone': '123123'}
        response = self.client.post('/user/register/', data)
        self.assertEqual(response.status_code, 200)

    def test_register_already_registered_user(self):
        data = {
            'username': 'user',
            'password': '123123',
            'email': 'Hi@there.com',
            'first_name': 'dima',
            'last_name': 'k',
            'city': 'Kiev',
            'phone': '123123'}

        response = self.client.post('/user/register/', data)
        self.assertEqual(response.status_code, 400)

    def test_register_invalid_form(self):
        def test_register_alreadyRegistered_user(self):
            data = {
                'usesrname': 'user',
                'password': '123123',
                'email': 'Hi@there.com',
                'first_name': 'dima',
                'last_name': 'k',
                'city': 'Kiev',
                'phone': '123123'}
            response = self.client.post('/user/register/', data)
            self.assertEqual(response.status_code, 400)
