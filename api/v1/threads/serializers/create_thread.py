from django.utils.translation import gettext_lazy as _

from rest_framework import serializers

from users.models import User


class CreateThreadSerializerV1(serializers.Serializer):
    user = serializers.IntegerField()

    custom_errors = {
        'user_does_not_exist': _('User does not exist'),
    }

    def validate_user(self, value: int) -> User:
        user = User.objects.exclude(id=self.context['request'].user.id).filter(id=value).first()
        if user is None:
            raise serializers.ValidationError(self.custom_errors['user_does_not_exist'])
        return user
