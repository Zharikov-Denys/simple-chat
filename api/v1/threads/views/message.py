from rest_framework.permissions import IsAuthenticated
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework import status

from core.viewsets import ServiceViewSet
from threads.models import Thread, Message

from api.v1.threads.dtos import CreateMessageDTOV1, ReadMessagesDTOV1
from api.v1.threads.serializers import MessageSerializerV1
from api.v1.threads.services import CreateMessageServiceV1, ReadMessagesServiceV1, GetUnreadMessagesServiceV1
from api.v1.core.serializers import IdsSerializerV1, CountSerializerV1
from api.v1.core.dtos import RequestUserDTOV1


class MessageViewSetV1(ServiceViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = MessageSerializerV1

    def get_service_dto_class(self):
        if self.action == 'read_messages':
            return ReadMessagesDTOV1
        elif self.action == 'get_unread_messages':
            return RequestUserDTOV1
        return CreateMessageDTOV1

    def get_service_class(self):
        if self.action == 'read_messages':
            return ReadMessagesServiceV1
        elif self.action == 'get_unread_messages':
            return GetUnreadMessagesServiceV1
        return CreateMessageServiceV1

    def get_serializer_class(self):
        if self.action == 'read_messages':
            return IdsSerializerV1
        elif self.action == 'get_unread_messages':
            return CountSerializerV1
        return super().get_serializer_class()

    def get_thread(self) -> Thread:
        return get_object_or_404(
            Thread.objects.filter(participants__id=self.request.user.id),
            pk=self.kwargs['pk']
        )

    def get_service_dto_class_kwargs(self, service_dto_class, **kwargs) -> dict:
        dto_kwargs = super().get_service_dto_class_kwargs(service_dto_class, **kwargs)
        if self.action in ['service_create', 'read_messages']:
            dto_kwargs.update({
                'request_user': self.request.user,
                'thread': self.get_thread(),
            })
        elif self.action in ['get_unread_messages']:
            dto_kwargs.update({'request_user': self.request.user})
        return dto_kwargs

    def get_queryset(self):
        return (
            Message.objects
            .filter(
                thread_id=self.kwargs['pk'],
                thread__participants__id=self.request.user.id,
            )
            .select_related('sender')
            .order_by('-created')
        )

    def read_messages(self, request: Request, *args, **kwargs) -> Response:
        return self.perform_service_action(success_status_code=status.HTTP_201_CREATED)

    def get_unread_messages(self, request: Request, *args, **kwargs) -> Response:
        return self.perform_service_action(without_request_serializer=True)
