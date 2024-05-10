from django.utils.translation import gettext_lazy as _
from django.urls import reverse

from rest_framework.test import APITestCase
from rest_framework import status

from users.factories import UserFactory
from threads.factories import ThreadFactory, MessageFactory
from threads.models import Message

from api.v1.threads.tests.mixins import MessageMixinV1


class MessagesReadingTestsV1(MessageMixinV1, APITestCase):
    url_name = 'api:v1:threads:messages-read'

    @classmethod
    def setUpTestData(cls):
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

    def setUp(self):
        self.first_message = MessageFactory.create(thread=self.first_thread, sender=self.first_user)
        self.second_message = MessageFactory.create(thread=self.first_thread, sender=self.second_user)
        self.third_message = MessageFactory.create(thread=self.second_thread, sender=self.third_user)

    def get_url(self, thread_id: int) -> str:
        return reverse(self.url_name, kwargs={'pk': thread_id})

    def get_valid_request_data(self, **kwargs) -> dict:
        request_data = {
            'ids': [self.first_message.id, self.second_message.id, self.third_message.id],
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
                'ids': [_('This field is required.')],
            },
            response.data
        )

    def test_valid_response(self):
        self.client.force_authenticate(user=self.first_user)
        request_data = self.get_valid_request_data()
        response = self.client.post(self.get_url(self.first_thread.id), request_data)

        self.assertEqual(status.HTTP_201_CREATED, response.status_code)
        self.assertEqual('application/json', response.headers['Content-Type'])
        self.assertEqual(request_data, response.data)

    def test_updated_messages(self):
        self.client.force_authenticate(user=self.first_user)
        response = self.client.post(self.get_url(self.first_thread.id), self.get_valid_request_data())

        first_message_from_db = Message.objects.get(id=self.first_message.id)
        second_message_from_db = Message.objects.get(id=self.second_message.id)
        third_message_from_db = Message.objects.get(id=self.third_message.id)

        self.assertFalse(first_message_from_db.is_read)
        self.assertTrue(second_message_from_db.is_read)
        self.assertFalse(third_message_from_db.is_read)
