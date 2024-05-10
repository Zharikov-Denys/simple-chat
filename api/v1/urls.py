from django.urls import path, include


urlpatterns = [
    path('users/', include(('api.v1.users.urls', 'users'), namespace='users')),
    path('threads/', include(('api.v1.threads.urls', 'threads'), namespace='threads')),
]
