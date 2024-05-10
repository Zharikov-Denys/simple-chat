from django.utils import timezone

from threads.factories.thread import ThreadFactory
from threads.models import Message

import factory
from factory import fuzzy
from datetime import timedelta

from users.factories import UserFactory

start_date = timezone.now() - timedelta(days=365)
end_date = timezone.now()


class MessageFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Message

    sender = factory.SubFactory(UserFactory)
    thread = factory.SubFactory(ThreadFactory)
    text = fuzzy.FuzzyText(length=50)
    created = fuzzy.FuzzyDateTime(start_date, end_date)
