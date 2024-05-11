from wagtail import hooks

from threads.views import ThreadChooserViewSet


@hooks.register('register_admin_viewset')
def register_thread_chooser_viewset():
    return ThreadChooserViewSet('thread_chooser', url_prefix='thread-chooser')
