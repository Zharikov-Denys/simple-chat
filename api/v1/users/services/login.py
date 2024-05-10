from django.utils import timezone

from rest_framework.authtoken.models import Token

from core.services import BaseService

from api.v1.users.dtos import UserDTOV1, TokenDTOV1


class LoginServiceV1(BaseService):
    def execute(self, data: UserDTOV1) -> TokenDTOV1:
        user = data.user

        token, created = Token.objects.get_or_create(user=user)

        user.last_login = timezone.now()
        user.save()

        return TokenDTOV1(token=token.key)