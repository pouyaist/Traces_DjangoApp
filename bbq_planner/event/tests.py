from django.test import TestCase
from django.test.client import Client, RequestFactory

from datetime import date, timedelta
import json

from user.factories import UserProfileFactory, UserAuthFactory
from event.factories import EventFactory


class TestEventResource(TestCase):
    def setUp(self):
        self.client = Client()
        self.user_auth = UserAuthFactory(username="user", password="pass", email="user@gmail.com")
        self.user_auth.save()
        self.user = UserProfileFactory(user_auth = self.user_auth, phone = '0123456789', city = 'Eind')
        self.user.save()
        self.event = EventFactory(organizer = self.user)
        self.event.save()

    def test_post_successfully_created_event(self):
        self.client.login(username="user", password="pass")
        event = {
        'name': 'Rock and Roll',
        'category': 'BBQ',
        'event_date': str(date.today())
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

    def test_get_successfully_all_events(self):
        self.client.login(username="user", password="pass")
        response = self.client.get('/events/')
        self.assertEqual(response.status_code, 200)

    def test_get_user_is_not_loggedin(self):
        response = self.client.get('/events/')
        self.assertEqual(response.status_code, 401)
