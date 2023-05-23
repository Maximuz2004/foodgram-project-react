from colorfield.fields import ColorField
from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator
from django.db import models

User = get_user_model()


class Tag(models.Model):
    name = models.CharField(
        verbose_name='Название тега',
        unique=True,
        max_length=settings.STRING_MAX_LENGTH,
    )
    color = ColorField(
        verbose_name='цвет тега hex',
        max_length=settings.HEX_COLOR_LENGTH
    )
    slug = models.SlugField(
        verbose_name='Идентификатор',
        unique=True,
        max_length=settings.STRING_MAX_LENGTH,
    )

    class Meta:
        verbose_name = 'Тег'
        verbose_name_plural = 'Теги'
        ordering = ('name',)

    def __str__(self):
        return self.name


class Ingredient(models.Model):
    name = models.CharField(
        verbose_name='Название ингредиента',
        help_text='Введите название ингредиента',
        unique=True,
        max_length=settings.STRING_MAX_LENGTH,
        null=False,
        blank=False,
    )
    measurement_unit = models.CharField(
        verbose_name='Единица измерения',
        help_text='Введите единицу измерения',
        max_length=settings.STRING_MAX_LENGTH,
        null=False,
        blank=False,
    )

    class Meta:
        verbose_name = 'Ингредиент'
        verbose_name_plural = 'Ингредиенты'
        ordering = ('name',)

    def __str__(self):
        return f'{self.name}, {self.measurement_unit}'


class Recipe(models.Model):
    author = models.ForeignKey(
        User,
        verbose_name='Автор',
        on_delete=models.CASCADE,
        related_name='recipes',
    )
    name = models.CharField(
        verbose_name='Название рецепта',
        help_text='Введите название рецепта',
        max_length=settings.STRING_MAX_LENGTH,
    )
    image = models.ImageField(
        verbose_name='Картинка',
        upload_to='recipes/images/',
    )
    text = models.TextField(
        verbose_name='Описание рецепта',
        help_text='Опишите процесс приготовления',
    )
    ingredients = models.ManyToManyField(
        Ingredient,
        verbose_name='Ингредиенты',
        help_text='Введите ингредиенты',
        through='IngredientInRecipe',
    )
    tags = models.ManyToManyField(
        Tag,
        verbose_name='Теги',
        help_text='Введите теги',
    )
    cooking_time = models.PositiveSmallIntegerField(
        verbose_name='Время приготовления в минутах',
        validators=(
            MinValueValidator(
                settings.MIN_COOKING_TIME,
                message=settings.COOKING_TIME_ERROR_MESSAGE
            ),
        )
    )
    pub_date = models.DateTimeField(
        verbose_name='Дата публикации',
        auto_now_add=True
    )

    class Meta:
        verbose_name = 'Рецепт'
        verbose_name_plural = 'Рецепты'
        ordering = ('-pub_date',)

    def __str__(self):
        return self.name


class TagInRecipe(models.Model):
    recipe = models.ForeignKey(
        Recipe,
        verbose_name='Рецепт',
        on_delete=models.CASCADE,
        related_name='tag_recipe'
    )
    tag = models.ForeignKey(
        Tag,
        verbose_name='Тег',
        on_delete=models.CASCADE,
        related_name='tag_recipe'
    )

    class Meta:
        verbose_name = 'Тег рецепта',
        verbose_name_plural = 'Теги рецептов'

    def __str__(self):
        return f'{self.recipe.name} на {self.tag.name}'


class IngredientInRecipe(models.Model):
    recipe = models.ForeignKey(
        Recipe,
        verbose_name='Рецепт',
        on_delete=models.CASCADE,
        related_name='ingredient_recipe'
    )
    ingredient = models.ForeignKey(
        Ingredient,
        verbose_name='Ингредиент',
        on_delete=models.CASCADE,
        related_name='ingredient_recipe'
    )
    amount = models.PositiveSmallIntegerField(
        verbose_name='Количество ингредиента',
        help_text='Введите количество ингредиента',
        validators=(
            MinValueValidator(
                settings.MIN_AMOUNT_VALUE,
                message=settings.AMOUNT_VALUE_ERROR_MESSAGE
            ),
        )
    )

    class Meta:
        verbose_name = 'Количество ингредиента'
        verbose_name_plural = 'Количество ингредиентов'

    def __str__(self):
        return (f'{self.ingredient.name} - {self.amount}'
                f' {self.ingredient.measurement_unit}')


class ShoppingCart(models.Model):
    user = models.ForeignKey(
        User,
        verbose_name='Пользователь',
        on_delete=models.CASCADE,
        related_name='shopping_cart_user',
    )
    recipe = models.ForeignKey(
        Recipe,
        verbose_name='Рецепт',
        on_delete=models.CASCADE,
        related_name='shopping_cart_recipe',
    )

    class Meta:
        verbose_name = 'Список покупок'
        verbose_name_plural = 'Список покупок'
        constraints = (
            models.UniqueConstraint(
                fields=('recipe', 'user'),
                name='unique_shopping_cart'
            ),
        )

    def __str__(self):
        return f'{self.recipe.name} в списке покупок у {self.user.username}'


class Favorites(models.Model):
    user = models.ForeignKey(
        User,
        verbose_name='Пользователь',
        on_delete=models.CASCADE,
        related_name='favorite_user',
    )
    recipe = models.ForeignKey(
        Recipe,
        verbose_name='Рецепт',
        on_delete=models.CASCADE,
        related_name='favorite_recipe'
    )

    class Meta:
        verbose_name = 'Избранное'
        verbose_name_plural = 'Избранные'
        constraints = (
            models.UniqueConstraint(
                fields=('recipe', 'user'),
                name='unique_favorites'
            ),
        )

    def __str__(self):
        return f'{self.recipe.name} в избранном у {self.user.username}'