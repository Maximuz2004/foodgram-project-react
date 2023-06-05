from django.contrib import admin


class EmptyFieldMixin(admin.ModelAdmin):
    empty_value_display = '-пусто-'
