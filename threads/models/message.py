from django.db import models
from django.utils.translation import gettext_lazy as _
from django.utils import timezone

from threads.managers import MessageManager


class Message(models.Model):
    thread = models.ForeignKey('threads.Thread', on_delete=models.CASCADE, related_name='messages', verbose_name=_('Thread'))
    sender = models.ForeignKey('users.User', on_delete=models.CASCADE, related_name='messages', verbose_name=_('Sender'))
    text = models.TextField(verbose_name=_('Text'))
    is_read = models.BooleanField(default=False, verbose_name=_('Read'))
    created = models.DateTimeField(default=timezone.now, verbose_name=_('Created'))

    objects = MessageManager()

    class Meta:
        verbose_name = _('Message')
        verbose_name_plural = _('Messages')
