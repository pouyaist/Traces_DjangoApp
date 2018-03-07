import json
from datetime import timedelta
from django.test import TestCase
from django.test.client import Client, RequestFactory
from user.factories import UserAuthFactory, UserProfileFactory
from food.factories import FoodFactory
from event.factories import EventFactory


class TestRegister(TestCase):
    def setUp(self):
        self.user_auth = UserAuthFactory(username="user", password="pass"
                , email="user@gmail.com")
        self.user_auth.save()
        self.user = UserProfileFactory(user_auth = self.user_auth
                , phone = '0123456789', city = 'Eind')
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


class TestEventAttendeeResource(TestCase):
    def setUp(self):
        self.client = Client()
        self.user_auth = UserAuthFactory(username="user", password="pass",
            email="user@gmail.com")
        self.user_auth.save()
        self.user = UserProfileFactory(user_auth = self.user_auth,
            phone = '0123456789', city = 'Eind')
        self.user.save()

        self.food = FoodFactory()
        self.food.save()

        self.food_chicken = FoodFactory(food_type="Chicken")
        self.food_chicken.save()

        self.event = EventFactory(organizer = self.user)
        self.event.save()
        self.event.food_types.add(self.food)
        self.event.food_types.add(self.food_chicken)

        self.event_date =  str(self.event.event_date)

        self.data = {
            'first_name' : 'Pouya',
            'last_name' : 'Samadi Khah',
            'number_of_guests': '5',
            'beef': '4',
            'pork': '5'
            }

    def test_post_successfully_created_attendee(self):
        response = self.client.post(
          f"/user/attend/{self.event_date }/{self.event.name}",
          json.dumps(self.data), content_type='application/json')
        self.assertEqual(response.status_code, 200)

    def test_post_invalid_event_date(self):
        event_date = str(self.event.event_date - timedelta(days = -1))
        response = self.client.post(
          f"/user/attend/{event_date}/{self.event.name}",
          json.dumps(self.data), content_type='application/json')
        self.assertEqual(response.status_code, 404)

    def test_post_invalid_event_name(self):
        response = self.client.post(
          f"/user/attend/{self.event_date }/wrong",
          json.dumps(self.data), content_type='application/json')
        self.assertEqual(response.status_code, 404)

    def test_post_invalid_format_guests(self):
        self.data['number_of_guests'] = 'invalid'
        response = self.client.post(
          f"/user/attend/{self.event_date }/{self.event.name}",
          json.dumps(self.data), content_type='application/json')
        self.assertEqual(response.status_code, 400)

    def test_post_invalid_format_first_name(self):
        self.data['first_name'] = None
        response = self.client.post(
          f"/user/attend/{self.event_date }/{self.event.name}",
          json.dumps(self.data), content_type='application/json')
        self.assertEqual(response.status_code, 400)

    def test_post_invalid_format_last_name(self):
        self.data['last_name'] = None
        response = self.client.post(
          f"/user/attend/{self.event_date }/{self.event.name}",
          json.dumps(self.data), content_type='application/json')
        self.assertEqual(response.status_code, 400)

    def test_post_empty_food_orders_attendee(self):
        self.data = {
            'first_name' : 'Pouya',
            'last_name' : 'Samadi Khah',
            'number_of_guests': '5',
            }
        response = self.client.post(
          f"/user/attend/{self.event_date }/{self.event.name}",
          json.dumps(self.data), content_type='application/json')
        self.assertEqual(response.status_code, 400)
