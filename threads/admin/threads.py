from wagtail.contrib.modeladmin.options import ModelAdmin, ModelAdminGroup

from django.utils.translation import gettext_lazy as _

from threads.models import Thread, Message


class ThreadAdmin(ModelAdmin):
    model = Thread
    menu_label = _('Thread')
    list_display = ['id', 'created', 'updated']
    list_filter = ['created', 'updated']
    menu_order = 1
    inspect_view_enabled = True


class MessageAdmin(ModelAdmin):
    model = Message
    menu_label = _('Message')
    list_display = ['id', 'thread', 'sender', 'text', 'is_read', 'created']
    list_filter = ['is_read', 'created']
    search_fields = ['user__username', 'user__email', 'text']
    menu_order = 2
    inspect_view_enabled = True


class ThreadsAdminGroup(ModelAdminGroup):
    menu_order = 100
    menu_label = _('Threads')
    items = [ThreadAdmin, MessageAdmin]
