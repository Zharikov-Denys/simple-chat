from django.utils.translation import gettext_lazy as _

from rest_framework import serializers

from api.v1.users.fields import PasswordFieldV1
from users.models import User


class RegistrationSerializerV1(serializers.ModelSerializer):
    password = PasswordFieldV1()

    class Meta:
        model = User
        fields = ['username', 'email', 'password']

    def validate_email(self, email: str) -> str:
        if User.objects.all().filter(email=email).exists():
            raise serializers.ValidationError(_('User with this Email already exists.'))
        return email
