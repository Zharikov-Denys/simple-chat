from rest_framework.serializers import DateTimeField

from api.v1.users.tests.mixins import UserMixinV1

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from threads.models import Message


class MessageMixinV1(UserMixinV1):
    def serialize_message(self, message: 'Message') -> dict:
        return {
            'id': message.id,
            'sender': self.serialize_user(message.sender),
            'text': message.text,
            'created': DateTimeField().to_representation(message.created),
            'is_read': message.is_read,
        }

    def serialize_multiple_messages(self, messages: list['Message']) -> list[dict]:
        return [self.serialize_message(message) for message in messages]