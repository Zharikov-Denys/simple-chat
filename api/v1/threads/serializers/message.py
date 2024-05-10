from rest_framework import serializers

from threads.models import Message

from api.v1.users.serializers import UserSerializerV1


class MessageSerializerV1(serializers.ModelSerializer):
    sender = UserSerializerV1(read_only=True)

    class Meta:
        model = Message
        fields = ['id', 'sender', 'text', 'is_read', 'created']
        read_only_fields = ['id', 'sender', 'is_read', 'created']
