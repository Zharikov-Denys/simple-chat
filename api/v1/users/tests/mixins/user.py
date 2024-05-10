from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from users.models import User


class UserMixinV1:
    def serialize_user(self, user: 'User') -> dict:
        return {
            'id': user.id,
            'username': user.username,
        }

    def serialize_multiple_users(self, users: list['User']) -> list[dict]:
        return [self.serialize_user(user) for user in users]
