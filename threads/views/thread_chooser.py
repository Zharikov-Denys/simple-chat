from django.utils.translation import gettext_lazy as _
from django.db.models import Q

from generic_chooser.views import ModelChooserViewSet, ModelChooserMixin

from threads.models import Thread

from typing import Optional


class ThreadChooserMixin(ModelChooserMixin):
    @property
    def is_searchable(self) -> bool:
        return True

    def get_unfiltered_object_list(self):
        objects = super().get_unfiltered_object_list()
        return objects.prefetch_participants().order_by('-id')

    def get_object_string(self, instance: Thread) -> str:
        return f'{instance.id} | {instance.created} | {instance.updated}'

    def user_can_create(self, user: Thread) -> bool:
        return False

    def get_object_list(self, search_term: Optional[str] = None, **kwargs):
        object_list = self.get_unfiltered_object_list()

        if search_term:
            object_list = (
                object_list
                .filter(
                    Q(paticipants__username__icontains=search_term)
                    | Q(paticipants__email__icontains=search_term)
                )
            )

        return object_list


class ThreadChooserViewSet(ModelChooserViewSet):
    model = Thread
    chooser_mixin_class = ThreadChooserMixin
    page_title = _('Choose a thread')
    per_page = 15
