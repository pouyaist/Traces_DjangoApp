import django.contrib.auth.models
import factory

from user.models import UserProfile, Attendee
from food.factories import FoodOrderFactory


class UserAuthFactory(factory.Factory):
    class Meta:
        model = django.contrib.auth.models.User

    username = factory.Sequence(lambda n: 'UserName{}'.format(n))
    first_name = factory.Sequence(lambda n: 'John{}'.format(n))
    last_name = 'Wick'
    is_active = True
    email = factory.Sequence(lambda n: 'John{}@sendcloud.com'.format(n))
    password = factory.PostGenerationMethodCall('set_password', 'password')


class UserProfileFactory(factory.Factory):
    class Meta:
        model = UserProfile
    user_auth= factory.SubFactory(UserAuthFactory)
    city = factory.Sequence(lambda n: 'City{}'.format(n))
    phone = factory.Sequence(lambda n: 'Phone{}'.format(n))


class AttendeeFactory(factory.Factory):
    class Meta:
        model = Attendee

    first_name = factory.Sequence(lambda n: 'John{}'.format(n))
    last_name = 'Wick'
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
