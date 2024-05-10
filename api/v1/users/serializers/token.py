from rest_framework import serializers


class TokenSerializerV1(serializers.Serializer):
    token = serializers.CharField()
