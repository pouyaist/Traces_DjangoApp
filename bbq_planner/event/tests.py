from django.test import TestCase
from django.test.client import Client

from datetime import date, timedelta
import json

from user.factories import UserProfileFactory, UserAuthFactory, AttendeeFactory
from event.factories import EventFactory, EventAttendeeFactory
from food.factories import FoodFactory, FoodOrderFactory
from food.serializers import FoodSerializer


class TestEventItemResource(TestCase):
    def setUp(self):
        self.client = Client()
        self.user_auth = UserAuthFactory(username="user", password="pass",
            email="user@gmail.com")
        self.user_auth.save()
        self.user = UserProfileFactory(user_auth = self.user_auth,
            phone = '0123456789', city = 'Eind')
        self.user.save()
        self.event = EventFactory.create(organizer = self.user)
        self.event.save()

        self.food = FoodFactory()
        self.food.save()

        self.food_chicken = FoodFactory(food_type="Chicken")
        self.food_chicken.save()

        self.event.food_types.add(self.food)
        self.event.food_types.add(self.food_chicken)

    def test_post_successfully_created_event(self):
        self.client.login(username="user", password="pass")
        event = {
        'name': 'Rock and Roll',
        'category': 'BBQ',
        'event_date': str(date.today()),
        'food_types': [self.food.id, self.food_chicken.id]
        }
        response = self.client.post('/events/item/', json.dumps(event),
         content_type='application/json')
        self.assertEqual(response.status_code, 201)

    def test_post_not_logged_in_created_event(self):

        event = {
        'name': 'Rock and Roll',
        'category': 'BBQ',
        'event_date': str(date.today())
        }
        response = self.client.post('/events/item/', json.dumps(event),
         content_type='application/json')
        self.assertEqual(response.status_code, 401)

    def test_post_create_already_created_event(self):
        self.client.login(username="user", password="pass")
        event = {
        'name': self.event.name,
        'category': self.event.category,
        'event_date': str(self.event.event_date)
        }
        response = self.client.post('/events/item/', json.dumps(event),
         content_type='application/json')
        self.assertEqual(response.status_code, 400)

    def test_post_wrong_date(self):
        self.client.login(username="user", password="pass")
        event = {
        'name': 'Rock and Roll',
        'category': 'BBQ',
        'event_date': str(date.today() - timedelta(days=1))
        }
        response = self.client.post('/events/item/', json.dumps(event),
         content_type='application/json')
        self.assertEqual(response.status_code, 400)


class TestEventResource(TestCase):
    def setUp(self):
        self.client = Client()
        self.user_auth = UserAuthFactory(username="user", password="pass",
            email="user@gmail.com")
        self.user_auth.save()
        self.user = UserProfileFactory(user_auth = self.user_auth,
            phone = '0123456789', city = 'Eind')
        self.user.save()
        self.event = EventFactory(organizer = self.user)
        self.event.save()

        self.food = FoodFactory()
        self.food.save()

        self.food_chicken = FoodFactory(food_type="Chicken")
        self.food_chicken.save()

        self.event.food_types.add(self.food)
        self.event.food_types.add(self.food_chicken)

    def test_get_successfully_all_events(self):
        self.client.login(username="user", password="pass")
        response = self.client.get('/events/')
        event_date = str(self.event.event_date)
        event = response.data['events'][0]
        self.assertEqual(response.status_code, 200)
        self.assertEqual(event['name'], self.event.name)
        self.assertEqual(event['organizer_name'],
                        self.event.organizer.user_auth.get_full_name())
        self.assertEqual(event['category'], self.event.category)
        self.assertEqual(event['number_of_attendees'], 0)
        self.assertEqual(event['event_date'], event_date)
        self.assertEqual(len(event['food_types']), 2)

    def test_get_user_is_not_loggedin(self):
        response = self.client.get('/events/')
        self.assertEqual(response.status_code, 401)


class TestEventInstanceResource(TestCase):
    def setUp(self):
        self.client = Client()
        self.user_auth = UserAuthFactory(username="user", password="pass",
            email="user@gmail.com")
        self.user_auth.save()
        self.user = UserProfileFactory(user_auth = self.user_auth,
            phone = '0123456789', city = 'Eind')
        self.user.save()
        self.event = EventFactory(organizer = self.user)
        self.event.save()

        self.food = FoodFactory()
        self.food.save()

        self.food_chicken = FoodFactory(food_type="Chicken")
        self.food_chicken.save()

        self.food_order_1 = FoodOrderFactory(food = self.food_chicken)
        self.food_order_1.save()

        self.food_order_2 = FoodOrderFactory(food = self.food)
        self.food_order_2.save()

        self.attendee = AttendeeFactory()
        self.attendee.save()

        self.event_attendee = EventAttendeeFactory(event = self.event,
                                                attendee = self.attendee)
        self.event_attendee.save()

        self.event_attendee.food_orders.add(self.food_order_1)
        self.event_attendee.food_orders.add(self.food_order_2)

    def test_get_wrong_date_event(self):
        event_date = str(self.event.event_date - timedelta(days = 10))
        response = self.client.get(f"/events/item/{event_date}/{self.event.name}")
        self.assertEqual(response.status_code, 404)

    def test_get_wrong_event_name(self):
        event_date = str(self.event.event_date)
        response = self.client.get(f"/events/item/{event_date}/wrong")
        self.assertEqual(response.status_code, 404)

    def test_get_successfully_event(self):
        event_date = str(self.event.event_date)
        response = self.client.get(f"/events/item/{event_date}/{self.event.name}")
        self.assertEqual(response.status_code, 200)
        data = response.data.get('event')
        self.assertEqual(data['name'], self.event.name)
        self.assertEqual(data['event_date'], event_date)
        self.assertEqual(data['organizer_name'],
                        self.event.organizer.user_auth.get_full_name())
        self.assertEqual(data['category'], self.event.category)
        self.assertEqual(data['number_of_attendees'], 11)
        food_order_number_list = {'chicken': 5, 'pork': 5}
        self.assertEqual(data['food_order_number_list'],
                                       food_order_number_list)
