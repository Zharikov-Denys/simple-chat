from django.db import models
from django.utils.translation import gettext_lazy as _
from django.utils import timezone

from wagtail.admin.panels import FieldPanel

from threads.managers import MessageManager
from users.widgets.user_chooser import UserChooser
from threads.widgets import ThreadChooser


class Message(models.Model):
    thread = models.ForeignKey('threads.Thread', on_delete=models.CASCADE, related_name='messages', verbose_name=_('Thread'))
    sender = models.ForeignKey('users.User', on_delete=models.CASCADE, related_name='messages', verbose_name=_('Sender'))
    text = models.TextField(verbose_name=_('Text'))
    is_read = models.BooleanField(default=False, verbose_name=_('Read'))
    created = models.DateTimeField(default=timezone.now, verbose_name=_('Created'))

    objects = MessageManager()

    panels = [
        FieldPanel('thread', widget=ThreadChooser),
        FieldPanel('sender', widget=UserChooser),
        FieldPanel('text'),
        FieldPanel('is_read'),
        FieldPanel('created'),
    ]

    class Meta:
        verbose_name = _('Message')
        verbose_name_plural = _('Messages')
