from django.db.models import Q

from core.services import BaseService
from threads.models import Message

from api.v1.threads.dtos import ReadMessagesDTOV1


class ReadMessagesServiceV1(BaseService):
    def execute(self, data: ReadMessagesDTOV1) -> ReadMessagesDTOV1:
        (
            Message.objects
            .filter(
                ~Q(sender=data.request_user),
                thread=data.thread,
                is_read=False,
                id__in=data.ids
            )
            .update(is_read=True)
        )
        return data
