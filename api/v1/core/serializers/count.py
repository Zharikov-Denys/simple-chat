from rest_framework import serializers


class CountSerializerV1(serializers.Serializer):
    count = serializers.IntegerField()
