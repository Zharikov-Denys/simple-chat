from dataclasses import dataclass


@dataclass
class RegisterUserDTOV1:
    username: str
    email: str
    password: str
