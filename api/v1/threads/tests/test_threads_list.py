from django.utils.translation import gettext_lazy as _
from django.urls import reverse

from rest_framework.test import APITestCase
from rest_framework import status

from users.factories import UserFactory
from users.models import User
from threads.factories import ThreadFactory
from threads.models import Thread

from api.v1.threads.tests.mixins import ThreadMixinV1


class ThreadsListTestsV1(ThreadMixinV1, APITestCase):
    url = reverse('api:v1:threads:threads-list')

    @classmethod
    def setUpTestData(cls):
        cls.nonexistent_user_id = 999

        cls.first_user = UserFactory.create()
        cls.second_user = UserFactory.create()

        users = UserFactory.build_batch(100)
        User.objects.bulk_create(users)
        users = User.objects.exclude(id__in=[cls.first_user.id, cls.second_user.id])

        for user in users:
            for main_user in [cls.first_user, cls.second_user]:
                thread = ThreadFactory.create()
                thread.participants.add(main_user)
                thread.participants.add(user)
                thread.save()

    def test_authentication_is_required(self):
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual('application/json', response.headers['Content-Type'])
        self.assertEqual(
            {
                'detail': _('Authentication credentials were not provided.'),
            },
            response.data
        )

    def test_valid_response(self):
        self.client.force_authenticate(user=self.first_user)
        response = self.client.get(self.url, {'limit': 20, 'offset': 20})

        expected_response_data = {
            'count': 100,
            'next': f'http://testserver{self.url}?limit=20&offset=40',
            'previous': f'http://testserver{self.url}?limit=20',
            'results': self.serialize_multiple_threads(
                Thread.objects
                .filter(participants__id=self.first_user.id)
                .prefetch_participants()
                .distinct()
                .order_by('-created')[20:40]
            ),
        }

        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual('application/json', response.headers['Content-Type'])
        self.assertEqual(expected_response_data, response.data)
