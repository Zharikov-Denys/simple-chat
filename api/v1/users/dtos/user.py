from dataclasses import dataclass

from users.models import User


@dataclass
class UserDTOV1:
    user: User
