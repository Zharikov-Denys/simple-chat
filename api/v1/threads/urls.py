from django.urls import path, include

from api.v1.threads.views import (
    ThreadViewSetV1,
    MessageViewSetV1,
)


threads_list = ThreadViewSetV1.as_view({
    'get': 'list',
    'post': 'service_create',
})

threads_detail = ThreadViewSetV1.as_view({
    'delete': 'destroy',
})

messages_list = MessageViewSetV1.as_view({
    'get': 'list',
    'post': 'service_create',
})

messages_read = MessageViewSetV1.as_view({
    'post': 'read_messages',
})

unread_messages = MessageViewSetV1.as_view({
    'get': 'get_unread_messages'
})


urlpatterns = [
    path('', threads_list, name='threads-list'),
    path('<int:pk>/', include([
        path('', threads_detail, name='threads-detail'),
        path('messages/', include([
            path('', messages_list, name='messages-list'),
            path('read/', messages_read, name='messages-read'),
        ])),
    ])),
    path('unread-messages/', unread_messages, name='unread-messages'),
]
