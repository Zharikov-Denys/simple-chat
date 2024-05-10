from django.db.models.manager import Manager

from threads.querysets import MessageQuerySet


class MessageManager(Manager):
    _queryset_class = MessageQuerySet
