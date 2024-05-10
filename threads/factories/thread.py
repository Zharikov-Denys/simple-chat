from django.utils import timezone

from threads.models import Thread

import factory
from factory import fuzzy
from datetime import timedelta


start_date = timezone.now() - timedelta(days=365)
end_date = timezone.now()


class ThreadFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Thread

    created = fuzzy.FuzzyDateTime(start_date, end_date)
    updated = factory.LazyAttribute(lambda obj: obj.created)
