from wagtail import hooks

from users.views import UserChooserViewSet


@hooks.register('register_admin_viewset')
def register_user_chooser_viewset():
    return UserChooserViewSet('user_chooser', url_prefix='user-chooser')
