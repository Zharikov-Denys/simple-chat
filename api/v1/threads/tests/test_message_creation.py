from django.utils.translation import gettext_lazy as _
from django.urls import reverse
from django.utils import timezone

from rest_framework.test import APITestCase
from rest_framework import status

from users.factories import UserFactory
from threads.factories import ThreadFactory
from threads.models import Message

from api.v1.threads.tests.mixins import MessageMixinV1

from freezegun import freeze_time


class MessageCreationTestsV1(MessageMixinV1, APITestCase):
    url_name = 'api:v1:threads:messages-list'

    @classmethod
    def setUpTestData(cls):
        cls.valid_text = 'Test message'

        cls.nonexistent_thread_id = 9999

        cls.first_user = UserFactory.create()
        cls.second_user = UserFactory.create()
        cls.third_user = UserFactory.create()

        cls.first_thread = ThreadFactory.create()
        cls.first_thread.participants.add(cls.first_user)
        cls.first_thread.participants.add(cls.second_user)
        cls.first_thread.save()

        cls.second_thread = ThreadFactory.create()
        cls.second_thread.participants.add(cls.second_user)
        cls.second_thread.participants.add(cls.third_user)
        cls.second_thread.save()

    def get_url(self, thread_id: int) -> str:
        return reverse(self.url_name, kwargs={'pk': thread_id})

    def get_valid_request_data(self, **kwargs) -> dict:
        request_data = {
            'text': self.valid_text,
        }
        request_data.update(kwargs)
        return request_data

    def test_authentication_is_required(self):
        response = self.client.post(self.get_url(self.first_thread.id), {})

        self.assertEqual(status.HTTP_401_UNAUTHORIZED, response.status_code)
        self.assertEqual('application/json', response.headers['Content-Type'])
        self.assertEqual(
            {
                'detail': _('Authentication credentials were not provided.'),
            },
            response.data
        )

    def test_nonexistent_thread_id(self):
        self.client.force_authenticate(user=self.first_user)
        response = self.client.post(self.get_url(self.nonexistent_thread_id), self.get_valid_request_data())

        self.assertEqual(status.HTTP_404_NOT_FOUND, response.status_code)
        self.assertEqual('application/json', response.headers['Content-Type'])
        self.assertEqual({'detail': _('No Thread matches the given query.')}, response.data)

    def test_others_people_thread(self):
        self.client.force_authenticate(user=self.first_user)
        response = self.client.post(self.get_url(self.second_thread.id), self.get_valid_request_data())

        self.assertEqual(status.HTTP_404_NOT_FOUND, response.status_code)
        self.assertEqual('application/json', response.headers['Content-Type'])
        self.assertEqual({'detail': _('No Thread matches the given query.')}, response.data)

    def test_required_fields(self):
        self.client.force_authenticate(user=self.first_user)
        response = self.client.post(self.get_url(self.first_thread.id), {})

        self.assertEqual(status.HTTP_400_BAD_REQUEST, response.status_code)
        self.assertEqual('application/json', response.headers['Content-Type'])
        self.assertEqual(
            {
                'text': [_('This field is required.')],
            },
            response.data
        )

    def test_valid_response(self):
        self.client.force_authenticate(user=self.first_user)
        response = self.client.post(self.get_url(self.first_thread.id), self.get_valid_request_data())

        message = Message.objects.last()
        expected_response_data = self.serialize_message(message)

        self.assertEqual(status.HTTP_201_CREATED, response.status_code)
        self.assertEqual('application/json', response.headers['Content-Type'])
        self.assertEqual(expected_response_data, response.data)

    @freeze_time('2021-01-01 12:00:00')
    def test_created_message(self):
        self.client.force_authenticate(user=self.first_user)
        response = self.client.post(self.get_url(self.first_thread.id), self.get_valid_request_data())

        self.assertEqual(1, Message.objects.count())

        message = Message.objects.last()

        self.assertEqual(self.first_user, message.sender)
        self.assertEqual(self.first_thread, message.thread)
        self.assertEqual(self.valid_text, message.text)
        self.assertFalse(message.is_read)
        self.assertEqual(timezone.now(), message.created)
