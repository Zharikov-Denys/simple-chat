from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _

from rest_framework import serializers


User = get_user_model()


class LoginSerializerV1(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField()

    custom_errors = {
        'user_does_not_exist': _('User assigned to this email does not exist.'),
        'invalid_password': _('Invalid password'),
    }

    def validate(self, attrs: dict) -> dict:
        try:
            user = User.objects.get(email=attrs.get('email'))
        except User.DoesNotExist:
            raise serializers.ValidationError({
                'email': self.custom_errors['user_does_not_exist'],
            })
        else:
            attrs.update({
                'user': user,
            })

        if not user.check_password(attrs.get('password')):
            raise serializers.ValidationError({
                'password': self.custom_errors['invalid_password'],
            })

        return attrs