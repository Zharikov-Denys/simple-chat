from django.utils.translation import gettext_lazy as _
from django.urls import reverse

from rest_framework.test import APITestCase
from rest_framework import status

from users.factories import UserFactory
from threads.factories import ThreadFactory
from threads.models import Thread

from api.v1.threads.tests.mixins import ThreadMixinV1


class ThreadRemovalTestsV1(ThreadMixinV1, APITestCase):
    url_name = 'api:v1:threads:threads-detail'

    @classmethod
    def setUpTestData(cls):
        cls.nonexistent_thread_id = 999

        cls.first_user = UserFactory.create()
        cls.second_user = UserFactory.create()
        cls.third_user = UserFactory.create()

    def setUp(self):
        self.first_thread = ThreadFactory.create()
        self.first_thread.participants.add(self.first_user)
        self.first_thread.participants.add(self.second_user)
        self.first_thread.save()

        self.second_thread = ThreadFactory.create()
        self.second_thread.participants.add(self.second_user)
        self.second_thread.participants.add(self.third_user)
        self.second_thread.save()

    def get_url(self, thread_id: int) -> str:
        return reverse(self.url_name, kwargs={'pk': thread_id})

    def test_authentication_is_required(self):
        response = self.client.delete(self.get_url(self.first_thread.id))

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual('application/json', response.headers['Content-Type'])
        self.assertEqual(
            {
                'detail': _('Authentication credentials were not provided.'),
            },
            response.data
        )

    def test_nonexistent_thread(self):
        self.client.force_authenticate(self.first_user)
        response = self.client.delete(self.get_url(self.nonexistent_thread_id))

        self.assertEqual(status.HTTP_404_NOT_FOUND, response.status_code)
        self.assertEqual('application/json', response.headers['Content-Type'])
        self.assertEqual({'detail': _('No Thread matches the given query.')}, response.data)

    def test_thread_of_others_people(self):
        self.client.force_authenticate(self.first_user)
        response = self.client.delete(self.get_url(self.second_thread.id))

        self.assertEqual(status.HTTP_404_NOT_FOUND, response.status_code)
        self.assertEqual('application/json', response.headers['Content-Type'])
        self.assertEqual({'detail': _('No Thread matches the given query.')}, response.data)

    def test_valid_response(self):
        self.client.force_authenticate(self.first_user)
        response = self.client.delete(self.get_url(self.first_thread.id))

        self.assertEqual(status.HTTP_204_NO_CONTENT, response.status_code)
        self.assertIsNone(response.data)

    def test_thread_is_removed(self):
        self.client.force_authenticate(self.first_user)
        response = self.client.delete(self.get_url(self.first_thread.id))

        self.assertFalse(Thread.objects.filter(id=self.first_thread.id).exists())
