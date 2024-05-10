from django.db.models import Q

from core.services import BaseService
from threads.models import Thread

from api.v1.threads.dtos import CreateThreadDTOV1


class CreateThreadServiceV1(BaseService):
    def execute(self, data: CreateThreadDTOV1) -> Thread:
        thread = (
            Thread.objects
            .filter(participants__id=data.user.id)
            .filter(participants__id=data.request_user.id)
            .prefetch_participants()
            .first()
        )
        if thread is None:
            thread = Thread.objects.create()
            thread.participants.add(data.user)
            thread.participants.add(data.request_user)
            thread.save()

        return thread
