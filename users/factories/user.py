from django.contrib.auth import get_user_model
from django.utils import timezone

import factory
from factory import fuzzy
from random import randint
from datetime import timedelta


User = get_user_model()

start_date = timezone.now() - timedelta(days=365)
end_date = timezone.now()


class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User

    first_name = factory.Faker('first_name')
    last_name = factory.Faker('last_name')
    username = factory.LazyAttribute(lambda obj: f'{obj.first_name} {obj.last_name}')
    email = factory.Sequence(lambda index: f'test_email_{index}@email.com')
    date_joined = fuzzy.FuzzyDateTime(start_date, end_date)
    last_login = factory.LazyAttribute(lambda obj: obj.date_joined + timedelta(
        days=randint(1, 180),
        hours=randint(1, 23),
        minutes=randint(1, 59),
        seconds=randint(1, 59),
        milliseconds=randint(1, 99),
        microseconds=randint(1, 999),
    ))
    is_active = True
    is_staff = False
    is_superuser = False


class SuperuserFactory(UserFactory):
    is_active = True
    is_staff = True
    is_superuser = True