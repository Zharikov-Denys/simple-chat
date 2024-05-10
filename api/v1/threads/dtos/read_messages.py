from dataclasses import dataclass

from typing import TYPE_CHECKING


if TYPE_CHECKING:
    from users.models import User
    from threads.models import Thread


@dataclass
class ReadMessagesDTOV1:
    ids: list[int]
    request_user: 'User'
    thread: 'Thread'
