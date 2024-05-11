from django.utils.translation import gettext_lazy as _

from generic_chooser.widgets import AdminChooser


class UserChooser(AdminChooser):
    choose_one_text = _('Chose a user')
    choose_another_text = _('Choose another user')
    link_to_chosen_text = _('Edit this user')
    choose_modal_url_name = 'user_chooser:choose'
    show_edit_link = False
    show_create_link = False

    @property
    def model(self):
        from users.models.user import User
        return User
