from django.utils.translation import gettext_lazy as _
from django.urls import reverse
from django.utils import timezone

from rest_framework.test import APITestCase
from rest_framework import status
from rest_framework.authtoken.models import Token

from users.factories import UserFactory
from users.models import User

from api.v1.users.serializers import LoginSerializerV1

from freezegun import freeze_time


class LoginTestsV1(APITestCase):
    url = reverse('api:v1:users:login')

    @classmethod
    def setUpTestData(cls):
        cls.valid_email = 'test@email.com'
        cls.valid_password = 'Testpassword_123'

        cls.invalid_email = 'testemail.com'
        cls.nonexistent_email = 'test123@email.com'
        cls.invalid_password = 'testpassw'

        cls.user = UserFactory.create(email=cls.valid_email)
        cls.user.set_password(cls.valid_password)
        cls.user.save()

    @classmethod
    def get_valid_request_data(cls, **kwargs) -> dict:
        request_data = {
            'email': cls.valid_email,
            'password': cls.valid_password,
        }
        request_data.update(kwargs)
        return request_data

    def test_required_fields(self):
        response = self.client.post(self.url, {})

        self.assertEqual(status.HTTP_400_BAD_REQUEST, response.status_code)
        self.assertEqual('application/json', response.headers['Content-Type'])
        self.assertEqual(
            {
                'email': [_('This field is required.')],
                'password': [_('This field is required.')],
            },
            response.data
        )

    def test_invalid_email(self):
        response = self.client.post(self.url, self.get_valid_request_data(email=self.invalid_email))

        self.assertEqual(status.HTTP_400_BAD_REQUEST, response.status_code)
        self.assertEqual('application/json', response.headers['Content-Type'])
        self.assertEqual(
            {
                'email': [_('Enter a valid email address.')],
            },
            response.data
        )

    def test_nonexistent_email(self):
        response = self.client.post(self.url, self.get_valid_request_data(email=self.nonexistent_email))

        self.assertEqual(status.HTTP_400_BAD_REQUEST, response.status_code)
        self.assertEqual('application/json', response.headers['Content-Type'])
        self.assertEqual(
            {
                'email': [LoginSerializerV1.custom_errors['user_does_not_exist']],
            },
            response.data
        )

    def test_invalid_password(self):
        response = self.client.post(self.url, self.get_valid_request_data(password=self.invalid_password))

        self.assertEqual(status.HTTP_400_BAD_REQUEST, response.status_code)
        self.assertEqual('application/json', response.headers['Content-Type'])
        self.assertEqual(
            {
                'password': [LoginSerializerV1.custom_errors['invalid_password']],
            },
            response.data
        )

    def test_response_after_valid_request(self):
        response = self.client.post(self.url, self.get_valid_request_data())

        token = Token.objects.get(user=self.user)

        self.assertEqual(status.HTTP_201_CREATED, response.status_code)
        self.assertEqual('application/json', response.headers['Content-Type'])
        self.assertEqual(
            {
                'token': token.key,
            },
            response.data
        )

    @freeze_time('2021-01-01 12:00:00')
    def test_token_creation_after_valid_request(self):
        self.client.post(self.url, self.get_valid_request_data())

        token = Token.objects.get(user=self.user)

        self.assertEqual(timezone.now(), token.created)

    @freeze_time('2021-01-01 12:00:00')
    def test_user_last_login_after_valid_request(self):
        self.client.post(self.url, self.get_valid_request_data())

        user = User.objects.get(id=self.user.id)

        self.assertEqual(timezone.now(), user.last_login)
