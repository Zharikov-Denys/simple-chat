from django.db import models
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import AbstractUser

from users.managers import UserManager


class User(AbstractUser):
    email = models.EmailField(unique=True, verbose_name=_('Email'))
    username = models.CharField(
        max_length=150,
        help_text=_('150 characters or fewer. Letters, digits and @/./+/-/_ only.'),
        verbose_name=_('Username'),
    )

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = _('User')
        verbose_name_plural = _('Users')

    def __str__(self) -> str:
        return f'{self.email} | {self.username}'
