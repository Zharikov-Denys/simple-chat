from dataclasses import dataclass

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from users.models import User


@dataclass
class RequestUserDTOV1:
    request_user: 'User'
