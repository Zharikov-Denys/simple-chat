from django.db.models import Q

from core.services import BaseService
from threads.models import Message

from api.v1.core.dtos import RequestUserDTOV1, CountDTOV1


class GetUnreadMessagesServiceV1(BaseService):
    def execute(self, data: RequestUserDTOV1) -> CountDTOV1:
        return CountDTOV1(
            count=Message.objects
            .filter(
                ~Q(sender=data.request_user),
                is_read=False,
                thread__participants__id=data.request_user.id,
            )
            .distinct()
            .count()
        )
