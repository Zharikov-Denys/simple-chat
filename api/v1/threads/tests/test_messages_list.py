from django.utils.translation import gettext_lazy as _
from django.urls import reverse

from rest_framework.test import APITestCase
from rest_framework import status

from users.factories import UserFactory
from threads.factories import ThreadFactory, MessageFactory
from threads.models import Message

from api.v1.threads.tests.mixins import MessageMixinV1


class MessagesListTestsV1(MessageMixinV1, APITestCase):
    url_name = 'api:v1:threads:messages-list'

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

        messages_to_save: list[Message] = []
        for thread in [cls.first_thread, cls.second_thread]:
            for i in range(50):
                for user in thread.participants.all():
                    messages_to_save.append(MessageFactory.build(thread=thread, sender=user))

        Message.objects.bulk_create(messages_to_save)

    def get_url(self, thread_id: int) -> str:
        return reverse(self.url_name, kwargs={'pk': thread_id})

    def test_authentication_is_required(self):
        response = self.client.get(self.get_url(self.first_thread.id))

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
        response = self.client.get(self.get_url(self.nonexistent_thread_id))

        expected_response_data = {
            'count': 0,
            'next': None,
            'previous': None,
            'results': [],
        }

        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual('application/json', response.headers['Content-Type'])
        self.assertEqual(expected_response_data, response.data)

    def test_others_people_thread(self):
        self.client.force_authenticate(user=self.first_user)
        response = self.client.get(self.get_url(self.second_thread.id))

        expected_response_data = {
            'count': 0,
            'next': None,
            'previous': None,
            'results': [],
        }

        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual('application/json', response.headers['Content-Type'])
        self.assertEqual(expected_response_data, response.data)

    def test_valid_response(self):
        self.client.force_authenticate(user=self.first_user)
        url = self.get_url(self.first_thread.id)
        response = self.client.get(url, data={'limit': 20, 'offset': 20})

        expected_response_data = {
            'count': 100,
            'next': f'http://testserver{url}?limit=20&offset=40',
            'previous': f'http://testserver{url}?limit=20',
            'results': self.serialize_multiple_messages(
                Message.objects
                .filter(thread_id=self.first_thread.id)
                .select_related('sender')
                .order_by('-created')[20:40]
            ),
        }

        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual('application/json', response.headers['Content-Type'])
        self.assertEqual(expected_response_data, response.data)
