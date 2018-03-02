import json
from django.test import TestCase
from user.factories import UserProfileFactory, UserAuthFactory, AttendeeFactory
from django.test.client import Client, RequestFactory
from food.factories import FoodOrderFactory, FoodFactory
from user.serializers import AttendeeSerializer
from user.models import Attendee




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


class TestAttendee(TestCase):
    def setUp(self):
        self.food = FoodFactory()
        self.food.save()

        self.food_order_1 = FoodOrderFactory(food = self.food)
        self.food_order_1.save()

        self.food_order_2 = FoodOrderFactory(food = self.food)
        self.food_order_2.save()

        self.attendee = AttendeeFactory()
        self.attendee.save()
        self.attendee.food_orders.add(self.food_order_1)
        self.attendee.food_orders.add(self.food_order_2)
        self.client = Client()
        self.factory = RequestFactory()

    def test_post_successfully_created_attendee(self):
        data={
            'first_name': 'dima',
            'last_name': 'Kondro',
            'number_of_guests': 10,
            'food_orders': AttendeeSerializer(self.attendee).data['food_orders']
            }
        response = self.client.post('/user/attend/', json.dumps(data),
         content_type='application/json')
        self.assertEqual(response.status_code, 201)
        self.assertEqual(Attendee.objects.filter(first_name = 'dima',
         last_name = 'Kondro', number_of_guests = 10).exists(), True)

    def test_post_invalid_attendee(self):
        data={
            'first_name': 'dima',
            'last_name': 'Kondro',
            'number_of_guests': 10,
            'food_orders': 'asdas'
            }
        response = self.client.post('/user/attend/', json.dumps(data),
         content_type='application/json')
        self.assertEqual(response.status_code, 412)

    def test_post_empty_food_orders_attendee(self):
        data={
            'first_name': 'dima',
            'last_name': 'Kondro',
            'number_of_guests': 10,
            'food_orders': []
            }
        response = self.client.post('/user/attend/', json.dumps(data),
         content_type='application/json')
        self.assertEqual(response.status_code, 412)
