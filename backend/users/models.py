from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from django.db import models
from users.validators import (validate_non_reserved,
                              validate_username_allowed_chars)

ROLES_CHOICES = (
    (settings.ROLE_USER, 'Пользователь'),
    (settings.ROLE_ADMIN, 'Администратор'),
)


class User(AbstractUser):
    username = models.CharField(
        verbose_name='Логин',
        help_text='Введите логин',
        unique=True,
        max_length=settings.STRING_LENGTH,
        validators=(
            validate_non_reserved,
            validate_username_allowed_chars
        ),
        error_messages={'unique': 'Это имя уже занято!'}
    )
    email = models.EmailField(
        verbose_name='адрес электронной почты',
        help_text='введите адрес электронной почты',
        unique=True,
        max_length=settings.EMAIL_MAX_LENGTH,
        error_messages={'unique': 'Этот email уже зарегистрирован!'}
    )
    role = models.CharField(
        choices=ROLES_CHOICES,
        default=settings.ROLE_USER,
        max_length=max(len(role) for role, _ in ROLES_CHOICES)
    )
    first_name = models.CharField(
        verbose_name='Имя',
        help_text='Введите имя',
        max_length=settings.STRING_LENGTH,
        blank=True,
        null=False,
    )
    last_name = models.CharField(
        verbose_name='Фамилия',
        help_text='Введите фамилию',
        max_length=settings.STRING_LENGTH,
        blank=True,
        null=False,
    )
    password = models.CharField(
        verbose_name='Пароль',
        help_text='Введите пароль. Обязательно. Не более 150 символов',
        max_length=settings.STRING_LENGTH,
        validators=(validate_password,)
    )
    created = models.DateTimeField(
        verbose_name='Дата создания',
        auto_now_add=True
    )

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ('username', 'first_name', 'last_name', 'password')

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
        ordering = ('created',)
        constraints = (
            models.UniqueConstraint(
                fields=('email', 'username'),
                name='unique_user'
            ),
        )

    def __str__(self):
        return self.username

    @property
    def is_admin(self):
        return self.role == settings.ROLE_ADMIN


class Subscription(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='subscriber',
        verbose_name='Пользователь, который подписывается'
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='subscribed',
        verbose_name='Пользователь, на которого подписываются'
    )

    def __str__(self):
        return f'{self.user.username}->{self.author.username}'

    def clean(self):
        if self.user == self.author:
            raise ValidationError(settings.SELF_SUBSCRIPTION_ERROR)

    class Meta:
        constraints = (
            models.UniqueConstraint(
                fields=('user', 'author'),
                name='unique_follow'
            ),
        )
        verbose_name = 'Подписка'
        verbose_name_plural = 'Подписки'
