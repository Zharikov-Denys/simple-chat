from core.viewsets import ServiceViewSet

from api.v1.users.dtos import RegisterUserDTOV1
from api.v1.users.serializers import RegistrationSerializerV1, TokenSerializerV1
from api.v1.users.services import RegisterUserServiceV1


class RegisterUserViewSetV1(ServiceViewSet):
    service_dto_class = RegisterUserDTOV1
    service_class = RegisterUserServiceV1
    request_serializer_class = RegistrationSerializerV1
    response_serializer_class = TokenSerializerV1
