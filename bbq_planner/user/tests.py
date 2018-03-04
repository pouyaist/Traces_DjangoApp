import json
from django.test import TestCase
from user.factories import UserProfileFactory, UserAuthFactory, AttendeeFactory
from django.test.client import Client, RequestFactory
from food.factories import FoodOrderFactory, FoodFactory
from event.factories import EventFactory, EventAttendeeFactory
from event.serializers import EventAttendeeSerializer


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

        self.food_order_1 = FoodOrderFactory(food = self.food_chicken)
        self.food_order_1.save()

        self.food_order_2 = FoodOrderFactory(food = self.food)
        self.food_order_2.save()

        self.event = EventFactory(organizer = self.user)
        self.event.save()
        self.event.food_types.add(self.food)
        self.event.food_types.add(self.food_chicken)

        self.event_date =  str(self.event.event_date)

        self.attendee = AttendeeFactory()
        self.attendee.save()

        self.event_attendee = EventAttendeeFactory(event = self.event,
                                                attendee = self.attendee)
        self.event_attendee.save()

        self.event_attendee.food_orders.add(self.food_order_1)
        self.event_attendee.food_orders.add(self.food_order_2)


    #TODO update the successfully test
    def test_post_successfully_created_attendee(self):
        data = EventAttendeeSerializer(self.event_attendee).data
        response = self.client.post(
          f"/user/attend/{self.event_date }/{self.event.name}",
          json.dumps(data), content_type='application/json')
        self.assertEqual(response.status_code, 201)

    def test_post_invalid_format_guests(self):
        data = EventAttendeeSerializer(self.event_attendee).data
        data['number_of_guests'] = 'invalid'
        response = self.client.post(
          f"/user/attend/{self.event_date }/{self.event.name}",
          json.dumps(data), content_type='application/json')
        self.assertEqual(response.status_code, 412)

    def test_post_empty_food_orders_attendee(self):
        data = EventAttendeeSerializer(self.event_attendee).data
        data['food_orders'] = []
        response = self.client.post(
          f"/user/attend/{self.event_date }/{self.event.name}",
          json.dumps(data), content_type='application/json')
        self.assertEqual(response.status_code, 412)
