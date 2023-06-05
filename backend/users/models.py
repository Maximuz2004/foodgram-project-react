from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.password_validation import validate_password
from django.db import models

from users.validators import (validate_non_reserved,
                              validate_username_allowed_chars)


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
        error_messages={'unique': settings.USERNAME_ALREADY_TAKEN_MESSAGE},
        db_index=True
    )
    email = models.EmailField(
        verbose_name='адрес электронной почты',
        help_text='введите адрес электронной почты',
        unique=True,
        max_length=settings.EMAIL_MAX_LENGTH,
        error_messages={'unique': settings.EMAIL_ALREADY_TAKEN_MESSAGE},
        db_index=True
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


class Subscription(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='follower',
        verbose_name='Подписчик на автора рецепта'
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='following',
        verbose_name='Автор рецепта, на которого подписываются'
    )

    def __str__(self):
        return f'{self.user.username}->{self.author.username}'

    class Meta:
        ordering = ('-author_id',)
        constraints = (
            models.UniqueConstraint(
                fields=('user', 'author'),
                name='unique_follow'
            ),
            models.CheckConstraint(
                name='%(app_label)s_%(class)s_prevent_self_follow',
                check=~models.Q(user=models.F('author')),
            ),
        )
        verbose_name = 'Подписка'
        verbose_name_plural = 'Подписки'
