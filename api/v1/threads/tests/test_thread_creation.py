from django.utils.translation import gettext_lazy as _
from django.urls import reverse
from django.utils import timezone

from rest_framework.test import APITestCase
from rest_framework import status

from users.factories import UserFactory
from threads.factories import ThreadFactory
from threads.models import Thread

from api.v1.threads.serializers import CreateThreadSerializerV1
from api.v1.threads.tests.mixins import ThreadMixinV1

from freezegun import freeze_time


class ThreadCreateTestsV1(ThreadMixinV1, APITestCase):
    url = reverse('api:v1:threads:threads-list')

    @classmethod
    def setUpTestData(cls):
        cls.nonexistent_user_id = 999

        cls.first_user = UserFactory.create()
        cls.second_user = UserFactory.create()
        cls.third_user = UserFactory.create()

        cls.existing_thread = ThreadFactory.create()
        cls.existing_thread.participants.add(cls.first_user)
        cls.existing_thread.participants.add(cls.second_user)
        cls.existing_thread.save()

    def get_valid_request_data(self, **kwargs) -> dict:
        request_data = {
            'user': self.second_user.id,
        }
        request_data.update(kwargs)
        return request_data

    def test_authentication_is_required(self):
        response = self.client.post(self.url, {})

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual('application/json', response.headers['Content-Type'])
        self.assertEqual(
            {
                'detail': _('Authentication credentials were not provided.'),
            },
            response.data
        )

    def test_required_fields(self):
        self.client.force_authenticate(self.first_user)
        response = self.client.post(self.url, {})

        self.assertEqual(status.HTTP_400_BAD_REQUEST, response.status_code)
        self.assertEqual('application/json', response.headers['Content-Type'])
        self.assertEqual(
            {
                'user': [_('This field is required.')],
            },
            response.data
        )

    def test_nonexistent_user_id(self):
        self.client.force_authenticate(self.first_user)
        response = self.client.post(self.url, self.get_valid_request_data(user=self.nonexistent_user_id))

        self.assertEqual(status.HTTP_400_BAD_REQUEST, response.status_code)
        self.assertEqual('application/json', response.headers['Content-Type'])
        self.assertEqual({'user': [CreateThreadSerializerV1.custom_errors['user_does_not_exist']]}, response.data)

    def test_request_user_id(self):
        self.client.force_authenticate(self.first_user)
        response = self.client.post(self.url, self.get_valid_request_data(user=self.first_user.id))

        self.assertEqual(status.HTTP_400_BAD_REQUEST, response.status_code)
        self.assertEqual('application/json', response.headers['Content-Type'])
        self.assertEqual({'user': [CreateThreadSerializerV1.custom_errors['user_does_not_exist']]}, response.data)

    def test_valid_response(self):
        self.client.force_authenticate(self.first_user)
        response = self.client.post(self.url, self.get_valid_request_data(user=self.second_user.id))

        self.assertEqual(status.HTTP_201_CREATED, response.status_code)
        self.assertEqual('application/json', response.headers['Content-Type'])
        self.assertEqual(self.serialize_thread(self.existing_thread), response.data)

    def test_existing_thread_is_not_changed(self):
        self.client.force_authenticate(self.first_user)
        response = self.client.post(self.url, self.get_valid_request_data(user=self.second_user.id))

        thread_from_db = Thread.objects.all().prefetch_participants().get(id=self.existing_thread.id)

        self.assertEqual(self.existing_thread.id, thread_from_db.id)
        self.assertEqual(self.existing_thread.created, thread_from_db.created)
        self.assertEqual(self.existing_thread.updated, thread_from_db.updated)
        self.assertIn(self.first_user, thread_from_db.participants.all())
        self.assertIn(self.second_user, thread_from_db.participants.all())
        self.assertEqual(2, len(thread_from_db.participants.all()))

    @freeze_time('2021-01-01 12:00:00')
    def test_new_thread_is_created(self):
        self.client.force_authenticate(self.first_user)
        response = self.client.post(self.url, self.get_valid_request_data(user=self.third_user.id))

        self.assertEqual(2, Thread.objects.all().count())

        thread_from_db = Thread.objects.all().prefetch_participants().last()

        self.assertEqual(timezone.now(), thread_from_db.created)
        self.assertEqual(timezone.now(), thread_from_db.updated)
        self.assertIn(self.first_user, thread_from_db.participants.all())
        self.assertIn(self.third_user, thread_from_db.participants.all())
        self.assertEqual(2, len(thread_from_db.participants.all()))
