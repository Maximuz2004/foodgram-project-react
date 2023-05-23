from django.contrib import admin

from .mixins import EmptyFieldMixin
from .models import Subscription, User


@admin.register(User)
class UserAdmin(EmptyFieldMixin, admin.ModelAdmin):
    list_display = (
        'pk',
        'username',
        'email',
        'first_name',
        'last_name',
        'created',
    )
    search_fields = ('username', 'email')
    list_filter = ('username', 'email')


@admin.register(Subscription)
class SubscriptionAdmin(EmptyFieldMixin, admin.ModelAdmin):
    list_display = ('user', 'author')
    search_fields = ('user', 'author')
    list_filter = ('user', 'author')
