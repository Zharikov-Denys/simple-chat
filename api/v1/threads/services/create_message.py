from core.services import BaseService

from threads.models import Message

from api.v1.threads.dtos import CreateMessageDTOV1


class CreateMessageServiceV1(BaseService):
    def execute(self, data: CreateMessageDTOV1) -> Message:
        return Message.objects.create(
            sender=data.request_user,
            thread=data.thread,
            text=data.text,
        )
