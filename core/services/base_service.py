from typing import Optional


class BaseService:
    def __init__(self, context: Optional[dict] = None) -> None:
        self.context = context if context is not None else {}

    def execute(self, data):
        raise NotImplementedError

    async def async_execute(self, data):
        raise NotImplementedError
