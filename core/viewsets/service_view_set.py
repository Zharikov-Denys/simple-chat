from rest_framework.viewsets import ModelViewSet
from rest_framework import status
from rest_framework.response import Response
from rest_framework.request import Request

from core.services import BaseService

from dataclasses import fields


class ServiceViewSet(ModelViewSet):
    service_dto_class = None
    service_class = None
    request_serializer_class = None
    response_serializer_class = None

    def get_serializer_class(self):
        try:
            return super().get_serializer_class()
        except:
            return self.get_request_serializer_class()

    def get_service_dto_class(self):
        if self.service_dto_class is not None:
            return self.service_dto_class
        return NotImplementedError('You have to implement the get_service_dto_class method.')

    def get_service_class(self):
        if self.service_class is not None:
            return self.service_class
        raise NotImplementedError('You have to implement the get_service_class method.')

    def get_request_serializer_class(self):
        if self.request_serializer_class is not None:
            return self.request_serializer_class

        try:
            return self.get_serializer_class()
        except:
            pass

        raise NotImplementedError('You have to implement the get_request_serializer_class method.')

    def get_response_serializer_class(self):
        if self.response_serializer_class is not None:
            return self.response_serializer_class
        try:
            return self.get_request_serializer_class()
        except NotImplementedError:
            raise NotImplementedError(
                'You have to implement either the get_request_serializer_class method or '
                'the get_response_serializer_class method.'
            )

    def get_service_context(self) -> dict:
        return {}

    def get_request_serializer_context(self) -> dict:
        return self.get_serializer_context()

    def get_response_serializer_context(self) -> dict:
        return self.get_serializer_context()

    def get_service(self, *args, **kwargs) -> BaseService:
        service_class = self.get_service_class()
        kwargs.setdefault('context', self.get_service_context())
        return service_class(*args, **kwargs)

    def get_service_dto_class_kwargs(self, service_dto_class, **kwargs) -> dict:
        dto_kwargs = {}
        fields_names = [field.name for field in fields(service_dto_class)]
        for key, value in kwargs.items():
            if key in fields_names:
                dto_kwargs[key] = value
        return dto_kwargs

    def get_service_dto(self, **kwargs):
        service_dto_class = self.get_service_dto_class()
        dto_kwargs = self.get_service_dto_class_kwargs(service_dto_class, **kwargs)
        return service_dto_class(**dto_kwargs)

    def get_request_serializer(self, *args, **kwargs):
        serializer_class = self.get_request_serializer_class()
        kwargs.setdefault('context', self.get_request_serializer_context())
        return serializer_class(*args, **kwargs)

    def get_response_serializer(self, *args, **kwargs):
        serializer_class = self.get_response_serializer_class()
        kwargs.setdefault('context', self.get_response_serializer_context())
        return serializer_class(*args, **kwargs)

    def perform_service_action(
            self,
            success_status_code: int = status.HTTP_200_OK,
            many: bool = False,
            without_request_serializer: bool = False,
    ) -> Response:
        if self.request.method in ['PUT'] and not without_request_serializer:
            request_serializer = self.get_request_serializer(
                instance=self.get_object(),
                data=self.request.data,
            )
            request_serializer.is_valid(raise_exception=True)
            service_dto = self.get_service_dto(**request_serializer.validated_data)
        elif self.request.method not in ['GET', 'DELETE'] and not without_request_serializer:
            request_serializer = self.get_request_serializer(data=self.request.data)
            request_serializer.is_valid(raise_exception=True)
            service_dto = self.get_service_dto(**request_serializer.validated_data)
        else:
            service_dto = self.get_service_dto()

        service = self.get_service()
        service_result = service.execute(data=service_dto)

        if success_status_code == status.HTTP_204_NO_CONTENT or service_result is None:
            return Response(status=success_status_code)
        response_serializer = self.get_response_serializer(service_result, many=many)
        return Response(status=success_status_code, data=response_serializer.data)

    def service_retrieve(self, request: Request, *args, **kwargs) -> Response:
        return self.perform_service_action()

    def service_list(self, request: Request, *args, **kwargs) -> Response:
        return self.perform_service_action(many=True)

    def service_destroy(self, request: Request, *args, **kwargs) -> Response:
        return self.perform_service_action(success_status_code=status.HTTP_204_NO_CONTENT)

    def service_create(self, request: Request, *args, **kwargs) -> Response:
        return self.perform_service_action(success_status_code=status.HTTP_201_CREATED)

    def service_update(self, request: Request, *args, **kwargs) -> Response:
        return self.perform_service_action()
