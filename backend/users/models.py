from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.db import models

ROLES_CHOICES = (
    (settings.ROLE_USER, 'Пользователь'),
    (settings.ROLE_ADMIN, 'Администратор'),
)


class User(AbstractUser):
    username = models.CharField(
        unique=True,
        max_length=settings.STRING_MAX_LENGTH,
    )
    email = models.EmailField(
        unique=True,
        max_length=settings.EMAIL_MAX_LENGTH
    )
    role = models.CharField(
        choices=ROLES_CHOICES,
        default=settings.ROLE_USER,
        max_length=max(len(role) for role, _ in ROLES_CHOICES)
    )
    first_name = models.CharField(
        max_length=settings.STRING_MAX_LENGTH,
        blank=True,
        null=False,
    )
    last_name = models.CharField(
        max_length=settings.STRING_MAX_LENGTH,
        blank=True,
        null=False,
    )

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
        ordering = ('username',)

    def __str__(self):
        return self.username

    @property
    def is_admin(self):
        return self.role == settings.ROLE_ADMIN
