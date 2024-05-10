from django.db.models.manager import Manager

from threads.querysets import ThreadQuerySet


class ThreadManager(Manager):
    _queryset_class = ThreadQuerySet
