from django.contrib import admin

from users.mixins import EmptyFieldMixin
from .models import (Favorites, Ingredient, IngredientInRecipe, Recipe,
                     ShoppingCart, Tag, TagInRecipe)


class IngredientInRecipeInline(admin.TabularInline):
    model = IngredientInRecipe
    extra = 1


class TagInRecipeInLine(admin.TabularInline):
    model = TagInRecipe
    extra = 1


@admin.register(Ingredient)
class IngredientAdmin(EmptyFieldMixin, admin.ModelAdmin):
    list_display = ('name', 'measurement_unit',)
    search_fields = ('name',)
    list_filter = ('measurement_unit',)


@admin.register(Tag)
class TagAdmin(EmptyFieldMixin, admin.ModelAdmin):
    list_display = ('name', 'color', 'slug',)
    search_fields = ('name',)
    list_filter = ('name',)


@admin.register(Recipe)
class RecipeAdmin(EmptyFieldMixin, admin.ModelAdmin):
    list_display = (
        'id',
        'author',
        'name',
        'text',
        'cooking_time',
        'pub_date',
        'count_favorite'
    )
    search_fields = ('author__username', 'name',)
    list_filter = ('name', 'author', 'tags',)
    readonly_fields = ('count_favorite',)
    inlines = (IngredientInRecipeInline, TagInRecipeInLine)
    exclude = ('tags', 'ingredients')

    @staticmethod
    def count_favorite(obj):
        return obj.favorite_recipe.count()


@admin.register(Favorites)
class FavoriteAdmin(EmptyFieldMixin, admin.ModelAdmin):
    list_display = ('user', 'recipe',)
    search_fields = ('user',)
    list_filter = ('user',)


@admin.register(ShoppingCart)
class ShoppingCartAdmin(EmptyFieldMixin, admin.ModelAdmin):
    list_display = ('user', 'recipe',)
    search_fields = ('user',)
    list_filter = ('user',)
