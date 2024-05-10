from django.db import models
from django.utils.translation import gettext_lazy as _
from django.utils import timezone

from threads.managers import ThreadManager


class Thread(models.Model):
    participants = models.ManyToManyField('users.User', related_name='threads', verbose_name=_('Participants'))
    created = models.DateTimeField(default=timezone.now, verbose_name=_('Created'))
    updated = models.DateTimeField(default=timezone.now, verbose_name=_('Updated'))

    objects = ThreadManager()

    class Meta:
        verbose_name = _('Thread')
        verbose_name_plural = _('Threads')
