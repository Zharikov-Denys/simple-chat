from rest_framework.authtoken.models import Token

from core.services import BaseService
from users.models import User
from api.v1.users.dtos import RegisterUserDTOV1, TokenDTOV1


class RegisterUserServiceV1(BaseService):
    def execute(self, data: RegisterUserDTOV1) -> TokenDTOV1:
        user = self.__create_user(data=data)
        token = self.__create_token(user=user)
        return TokenDTOV1(token=token.key)

    def __create_user(self, data: RegisterUserDTOV1) -> User:
        return User.objects.create_user(
            username=data.username,
            email=data.email,
            password=data.password,
        )

    def __create_token(self, user: User) -> Token:
        return Token.objects.create(user=user)
