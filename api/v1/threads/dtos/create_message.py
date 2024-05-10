from dataclasses import dataclass

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from users.models import User
    from threads.models import Thread


@dataclass
class CreateMessageDTOV1:
    text: str
    request_user: 'User'
    thread: 'Thread'
