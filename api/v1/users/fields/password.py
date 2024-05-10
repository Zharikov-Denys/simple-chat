from rest_framework import serializers

from api.v1.users.validators import PasswordValidatorV1


class PasswordFieldV1(serializers.CharField):
    def __init__(self, **kwargs) -> None:
        kwargs.update({'max_length': 128})
        super().__init__(**kwargs)
        self.validators.append(PasswordValidatorV1())
