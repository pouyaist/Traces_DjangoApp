import factory
from datetime import date

from event.models import Event
from user.factories import UserProfileFactory


class EventFactory(factory.Factory):

    class Meta:
        model = Event

    name = factory.Sequence(lambda n: 'Evenname{}'.format(n))
    organizer = factory.SubFactory(UserProfileFactory)
    category = factory.Sequence(lambda n: 'Category{}'.format(n))
    event_date = date.today()
    url = factory.Sequence(lambda n: 'http://bbqplanner/event/{}'.format(n))
