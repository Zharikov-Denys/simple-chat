from rest_framework import serializers

from threads.models import Thread

from api.v1.users.serializers import UserSerializerV1


class ThreadSerializerV1(serializers.ModelSerializer):
    participants = UserSerializerV1(many=True, read_only=True)

    class Meta:
        model = Thread
        fields = ['id', 'participants', 'created', 'updated']
        read_only_fields = ['id', 'participants', 'created', 'updated']
