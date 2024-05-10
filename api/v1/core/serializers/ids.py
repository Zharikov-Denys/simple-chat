from rest_framework import serializers


class IdsSerializerV1(serializers.Serializer):
    ids = serializers.ListSerializer(child=serializers.IntegerField())
