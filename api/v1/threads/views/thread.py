from rest_framework.permissions import IsAuthenticated

from core.viewsets import ServiceViewSet
from threads.models import Thread

from api.v1.threads.dtos import CreateThreadDTOV1
from api.v1.threads.serializers import CreateThreadSerializerV1, ThreadSerializerV1
from api.v1.threads.services import CreateThreadServiceV1


class ThreadViewSetV1(ServiceViewSet):
    permission_classes = [IsAuthenticated]
    service_dto_class = CreateThreadDTOV1
    service_class = CreateThreadServiceV1
    request_serializer_class = CreateThreadSerializerV1
    response_serializer_class = ThreadSerializerV1
    serializer_class = ThreadSerializerV1

    def get_service_dto_class_kwargs(self, service_dto_class, **kwargs) -> dict:
        dto_kwargs = super().get_service_dto_class_kwargs(service_dto_class, **kwargs)
        if self.action == 'service_create':
            dto_kwargs.update({'request_user': self.request.user})
        return dto_kwargs

    def get_queryset(self):
        return (
            Thread.objects
            .filter(participants__id=self.request.user.id)
            .prefetch_participants()
            .distinct()
            .order_by('-created')
        )
