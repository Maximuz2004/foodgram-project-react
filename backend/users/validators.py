from django.conf import settings
from django.core.exceptions import ValidationError

ERROR_USERNAME_RESERVED = ("'{value}' нельзя использовать в качестве "
                           "имени пользователя")
ERROR_USERNAME_SYMBOL = "Нельзя использовать символы '{}' в username"


def validate_non_reserved(value):
    if value in settings.RESERVED_USERNAMES:
        raise ValidationError(ERROR_USERNAME_RESERVED.format(value=value))
    return value


def validate_username_allowed_chars(value):
    invalid_chars = settings.USERNAME_INVALID_PATTERN.findall(value)
    if invalid_chars:
        raise ValidationError(
            ERROR_USERNAME_SYMBOL.format(''.join(set(''.join(invalid_chars))))
        )
    return value
