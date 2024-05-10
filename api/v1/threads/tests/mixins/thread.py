from rest_framework.serializers import DateTimeField

from api.v1.users.tests.mixins import UserMixinV1

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from threads.models import Thread


class ThreadMixinV1(UserMixinV1):
    def serialize_thread(self, thread: 'Thread') -> dict:
        return {
            'id': thread.id,
            'participants': self.serialize_multiple_users(thread.participants.all()),
            'created': DateTimeField().to_representation(thread.created),
            'updated': DateTimeField().to_representation(thread.updated),
        }

    def serialize_multiple_threads(self, threads: list['Thread']) -> list[dict]:
        return [self.serialize_thread(thread) for thread in threads]
