from django.urls import path

from api.v1.users.views import (
    RegisterUserViewSetV1,
    LoginViewSetV1,
)


register_user = RegisterUserViewSetV1.as_view({'post': 'service_create'})

login = LoginViewSetV1.as_view({'post': 'service_create'})


urlpatterns = [
    path('register/', register_user, name='register'),
    path('login/', login, name='login'),
]
