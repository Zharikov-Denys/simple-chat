from django.utils.translation import gettext_lazy as _
from django.urls import reverse

from rest_framework.test import APITestCase
from rest_framework import status

from users.factories import UserFactory
from threads.factories import ThreadFactory, MessageFactory
from threads.models import Message

from api.v1.threads.tests.mixins import MessageMixinV1


class MessagesListTestsV1(MessageMixinV1, APITestCase):
    url = reverse('api:v1:threads:unread-messages')

    @classmethod
    def setUpTestData(cls):
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

        cls.third_thread = ThreadFactory.create()
        cls.third_thread.participants.add(cls.first_user)
        cls.third_thread.participants.add(cls.third_user)
        cls.third_thread.save()

        messages_to_save: list[Message] = []
        for thread in [cls.first_thread, cls.second_thread, cls.third_thread]:
            for i in range(25):
                for user in thread.participants.all():
                    messages_to_save.append(MessageFactory.build(thread=thread, sender=user, is_read=False))

            for i in range(25):
                for user in thread.participants.all():
                    messages_to_save.append(MessageFactory.build(thread=thread, sender=user, is_read=True))

        Message.objects.bulk_create(messages_to_save)

    def test_authentication_is_required(self):
        response = self.client.get(self.url)

        self.assertEqual(status.HTTP_401_UNAUTHORIZED, response.status_code)
        self.assertEqual('application/json', response.headers['Content-Type'])
        self.assertEqual(
            {
                'detail': _('Authentication credentials were not provided.'),
            },
            response.data
        )

    def test_valid_response(self):
        self.client.force_authenticate(user=self.first_user)
        response = self.client.get(self.url)

        expected_response_data = {
            'count': 50,
        }

        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual('application/json', response.headers['Content-Type'])
        self.assertEqual(expected_response_data, response.data)
