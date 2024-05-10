from django.utils.translation import gettext_lazy as _
from django.urls import reverse
from django.utils import timezone

from rest_framework.test import APITestCase
from rest_framework import status
from rest_framework.authtoken.models import Token

from users.factories import UserFactory
from users.models import User

from freezegun import freeze_time


class UserRegistrationTestsV1(APITestCase):
    url = reverse('api:v1:users:register')

    @classmethod
    def setUpTestData(cls) -> None:
        cls.valid_username = 'Test Username'
        cls.valid_email = 'test@email.com'
        cls.valid_password = 'Testpassword_123'

        cls.invalid_email = 'testemail.com'
        cls.short_password = 'test'

        cls.existing_user = UserFactory.create()

    def get_valid_request_data(self, **kwargs) -> dict:
        request_data = {
            'username': self.valid_username,
            'email': self.valid_email,
            'password': self.valid_password,
        }
        request_data.update(kwargs)
        return request_data

    def test_required_fields(self):
        response = self.client.post(self.url, {})

        self.assertEqual(status.HTTP_400_BAD_REQUEST, response.status_code)
        self.assertEqual('application/json', response.headers['Content-Type'])
        self.assertEqual(
            {
                'username': [_('This field is required.')],
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

    def test_short_password(self):
        response = self.client.post(self.url, self.get_valid_request_data(password=self.short_password))

        self.assertEqual(status.HTTP_400_BAD_REQUEST, response.status_code)
        self.assertEqual('application/json', response.headers['Content-Type'])
        self.assertEqual(
            {
                'password': [_('Password has to be at least 8 symbols length.')],
            },
            response.data
        )

    def test_duplicated_email(self):
        response = self.client.post(self.url, self.get_valid_request_data(email=self.existing_user.email))

        self.assertEqual(status.HTTP_400_BAD_REQUEST, response.status_code)
        self.assertEqual('application/json', response.headers['Content-Type'])
        self.assertEqual(
            {
                'email': [_('User with this Email already exists.')],
            },
            response.data
        )

    def test_response_after_valid_request(self):
        response = self.client.post(self.url, self.get_valid_request_data())

        token = Token.objects.first()

        self.assertEqual(status.HTTP_201_CREATED, response.status_code)
        self.assertEqual('application/json', response.headers['Content-Type'])
        self.assertEqual(
            {
                'token': token.key,
            },
            response.data
        )

    @freeze_time('2021-01-01 12:00:00')
    def test_user_creation_after_valid_request(self):
        self.client.post(self.url, self.get_valid_request_data())

        user = User.objects.get(email=self.valid_email)

        self.assertEqual(self.valid_username, user.username)
        self.assertEqual(self.valid_email, user.email)
        self.assertEqual(timezone.now(), user.date_joined)
        self.assertTrue(user.check_password(self.valid_password))

    @freeze_time('2021-01-01 12:00:00')
    def test_token_creation_after_valid_request(self):
        self.client.post(self.url, self.get_valid_request_data())

        token = Token.objects.get(user__email=self.valid_email)

        self.assertEqual(timezone.now(), token.created)
