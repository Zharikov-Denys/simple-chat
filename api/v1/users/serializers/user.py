from rest_framework import serializers

from users.models import User


class UserSerializerV1(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username']
