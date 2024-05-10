from core.viewsets import ServiceViewSet

from api.v1.users.dtos import UserDTOV1
from api.v1.users.serializers import LoginSerializerV1, TokenSerializerV1
from api.v1.users.services import LoginServiceV1


class LoginViewSetV1(ServiceViewSet):
    service_dto_class = UserDTOV1
    service_class = LoginServiceV1
    request_serializer_class = LoginSerializerV1
    response_serializer_class = TokenSerializerV1