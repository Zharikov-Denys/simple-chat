from django.utils.translation import gettext_lazy as _

from generic_chooser.widgets import AdminChooser
from threads.models import Thread


class ThreadChooser(AdminChooser):
    choose_one_text = _('Choose a thread')
    choose_another_text = _('Choose another thread')
    link_to_chosen_text = _('Edit this thread')
    model = Thread
    choose_modal_url_name = 'thread_chooser:choose'
    show_edit_link = False
    show_create_link = False
