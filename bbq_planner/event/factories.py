import factory
from datetime import date

from event.models import Event, EventAttendee
from user.factories import UserProfileFactory, AttendeeFactory


class EventFactory(factory.Factory):

    class Meta:
        model = Event

    name = factory.Sequence(lambda n: 'Evenname{}'.format(n))
    organizer = factory.SubFactory(UserProfileFactory)
    category = factory.Sequence(lambda n: 'Category{}'.format(n))
    event_date = date.today()
    url = factory.Sequence(lambda n: 'http://bbqplanner/event/{}'.format(n))

    @factory.post_generation
    def food_types(self, create, extracted, **kwargs):
        if not create:
            # Simple build, do nothing.
            return

        if extracted:
            # A list of groups were passed in, use them
            for food in extracted:
                self.food_types.add(food_types)


class EventAttendeeFactory(factory.Factory):

    class Meta:
        model = EventAttendee

    event = factory.SubFactory(EventFactory)
    attendee = factory.SubFactory(AttendeeFactory)
    number_of_guests = 10

    @factory.post_generation
    def food_orders(self, create, extracted, **kwargs):
        if not create:
            # Simple build, do nothing.
            return

        if extracted:
            # A list of groups were passed in, use them
            for food_order in extracted:
                self.food_orders.add(food_order)
