from django.utils.translation import gettext_lazy as _
from django.db.models import Q

from generic_chooser.views import ModelChooserViewSet, ModelChooserMixin

from users.models.user import User

from typing import Optional


class UserChooserMixin(ModelChooserMixin):
    @property
    def is_searchable(self) -> bool:
        return True

    def get_unfiltered_object_list(self):
        objects = super().get_unfiltered_object_list()
        return objects.order_by('-id')

    def get_object_string(self, instance: User) -> str:
        return f'{instance.username} | {instance.email}'

    def user_can_create(self, user: User) -> bool:
        return False

    def get_object_list(self, search_term: Optional[str] = None, **kwargs):
        object_list = self.get_unfiltered_object_list()

        if search_term:
            object_list = (
                object_list
                .filter(
                    Q(username__icontains=search_term)
                    | Q(email__icontains=search_term)
                )
            )

        return object_list


class UserChooserViewSet(ModelChooserViewSet):
    model = User
    chooser_mixin_class = UserChooserMixin
    page_title = _('Choose a user')
    per_page = 15
