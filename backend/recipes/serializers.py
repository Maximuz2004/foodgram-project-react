from django.contrib.auth import get_user_model
from django.conf import settings
from drf_extra_fields.fields import Base64ImageField
from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator

from users.models import Subscription
from users.serializers import CustomUserSerializer

from .models import (Favorites, Ingredient, IngredientInRecipe, Recipe,
                     ShoppingCart, Tag)

User = get_user_model()


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ('id', 'name', 'color', 'slug')
        read_only_fields = '__all__',


class IngredientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ingredient
        fields = ('id', 'name', 'measurement_unit')
        read_only_fields = '__all__',


class IngredientInRecpeSerializer(serializers.ModelSerializer):
    id = serializers.ReadOnlyField(source='ingredient.id')
    name = serializers.ReadOnlyField(source='ingredient.name')
    measurement_unit = serializers.ReadOnlyField(
        source='ingredient.measurement_unit'
    )

    class Meta:
        model = IngredientInRecipe
        fields = ('id', 'name', 'measurement_unit', 'amount')


class AddIngredientSerializer(serializers.ModelSerializer):
    id = serializers.PrimaryKeyRelatedField(queryset=Ingredient.objects.all())
    amount = serializers.IntegerField()

    class Meta:
        model = IngredientInRecipe
        fields = ('id', 'amount')

    def validate_amount(self, value):
        if settings.MAX_AMOUNT_VALUE < int(value) < settings.MIN_AMOUNT_VALUE:
            raise serializers.ValidationError(
                settings.AMOUNT_VALUE_ERROR_MESSAGE
            )
        return value


class FavoritesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Favorites
        fields = ('user', 'recipe')

    def validate(self, data):
        request = self.context.get('request')
        if not request or request.user.is_anonymous:
            return False
        recipe = data['recipe']
        if request.user.favorite_user.filter(recipe=recipe).exists():
            raise serializers.ValidationError(
                settings.ALREADY_IN_FAVORITES_ERROR
            )
        return data

    def to_representation(self, instance):
        request = self.context.get('request')
        context = {'request': request}
        return FavoritePreviewSerializer(instance.recipe, context=context).data


class FavoritePreviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Recipe
        fields = ('id', 'name', 'image', 'cooking_time')


class RecipeViewSerializer(serializers.ModelSerializer):
    author = CustomUserSerializer(read_only=True)
    tags = TagSerializer(many=True)
    ingredients = serializers.SerializerMethodField(
        read_only=True,
        source='get_ingredients'
    )
    is_favorited = serializers.SerializerMethodField(
        read_only=True,
        source='get_is_favorited'
    )
    is_in_shopping_cart = serializers.SerializerMethodField(
        read_only=True,
        source='get_is_in_shopping_cart'
    )

    class Meta:
        model = Recipe
        fields = (
            'id',
            'tags',
            'author',
            'ingredients',
            'is_favorited',
            'is_in_shopping_cart',
            'name',
            'image',
            'text',
            'cooking_time'
        )

    def get_ingredients(self, obj):
        ingredients = IngredientInRecipe.objects.filter(recipe=obj)
        return IngredientInRecpeSerializer(ingredients, many=True).data

    def get_is_favorited(self, obj):
        request = self.context.get('request')
        if not request or request.user.is_anonymous:
            return False
        return request.user.favorite_user.filter(recipe=obj).exists()

    def get_is_in_shopping_cart(self, obj):
        request = self.context.get('request')
        if not request or request.user.is_anonymous:
            return False
        return request.user.shopping_cart_user.filter(recipe=obj).exists()


class RecipeCreateSerializer(serializers.ModelSerializer):
    tags = serializers.PrimaryKeyRelatedField(
        queryset=Tag.objects.all(),
        many=True
    )
    image = Base64ImageField()
    ingredients = AddIngredientSerializer(many=True)
    author = CustomUserSerializer(read_only=True)

    class Meta:
        model = Recipe
        fields = (
            'id',
            'tags',
            'author',
            'ingredients',
            'image',
            'name',
            'text',
            'cooking_time'
        )

    def validate(self, data):
        ingredients = self.initial_data.get('ingredients')
        ingredients_list = set()
        for ingredient in ingredients:
            ingredient_id = ingredient['id']
            if ingredient_id in ingredients_list:
                raise serializers.ValidationError(
                    settings.SAME_INGREDIENTS_ERROR
                )
            ingredients_list.add(ingredient_id)
            if (settings.MAX_AMOUNT_VALUE < int(ingredient['amount'])
                    <= settings.MIN_AMOUNT_VALUE):
                raise serializers.ValidationError(
                    settings.AMOUNT_VALUE_ERROR_MESSAGE
                )
        tags = self.initial_data.get('tags')
        if not tags:
            raise serializers.ValidationError(settings.NO_TAGS_ERROR)
        tags_list = []
        for tag in tags:
            if tag in tags_list:
                raise serializers.ValidationError(
                    settings.SAME_TAGS_ERROR
                )
            tags_list.append(tag)
        if (
                settings.MAX_COOKING_TIME
                < int(self.initial_data.get('cooking_time'))
                <= settings.MIN_COOKING_TIME
        ):
            raise serializers.ValidationError(
                settings.COOKING_TIME_ERROR_MESSAGE
            )
        return data

    def create_ingredients(self, recipe, ingredients):
        IngredientInRecipe.objects.bulk_create(
            [
                IngredientInRecipe(
                    recipe=recipe,
                    ingredient=ingredient['id'],
                    amount=ingredient['amount']
                )
                for ingredient in ingredients
            ]
        )

    def create(self, validated_data):
        request = self.context.get('request')
        ingredients = validated_data.pop('ingredients', None)
        tags = validated_data.pop('tags', None)
        recipe = Recipe.objects.create(author=request.user, **validated_data)
        recipe.tags.set(tags)
        self.create_ingredients(recipe, ingredients)
        return recipe

    def update(self, instance, validated_data):
        ingredients = validated_data.pop('ingredients')
        tags = validated_data.pop('tags')
        instance.name = validated_data.get('name', instance.name)
        instance.text = validated_data.get('text', instance.text)
        instance.image = validated_data.get('image', instance.image)
        instance.cooking_time = validated_data.get(
            'cooking_time',
            instance.cooking_time
        )
        if tags:
            instance.tags.set(tags)
        if ingredients:
            IngredientInRecipe.objects.filter(recipe=instance).delete()
            self.create_ingredients(instance, ingredients)
        instance.save()
        return instance

    def to_representation(self, instance):
        return RecipeViewSerializer(
            instance,
            context={'request': self.context.get('request')}
        ).data


class FollowSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subscription
        fields = ('user', 'author')
        validators = (
            UniqueTogetherValidator(
                queryset=Subscription.objects.all(),
                fields=('user', 'author'),
                message=settings.SAME_SUBSCRIPTION_ERROR
            ),
        )

    def validate(self, data):
        user = data.get('user')
        author = data.get('author')
        if user == author:
            raise serializers.ValidationError(settings.SELF_SUBSCRIPTION_ERROR)
        return data

    def to_representation(self, instance):
        return SubscriptionSerializer(
            instance.author,
            context={'request': self.context.get('request')}

        ).data


class FollowRecipeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Recipe
        fields = ('id', 'name', 'image', 'cooking_time')
        ordering = ('id',)

    def to_representation(self, instance):
        return RecipeViewSerializer(instance).data


class SubscriptionSerializer(serializers.ModelSerializer):
    is_subscribed = serializers.SerializerMethodField(
        source='get_is_subscribed'
    )
    recipes = serializers.SerializerMethodField(
        source='get_recipes'
    )
    recipes_count = serializers.SerializerMethodField(
        source='get_recipes_count'
    )

    class Meta:
        model = User
        fields = (
            'email',
            'id',
            'username',
            'first_name',
            'last_name',
            'is_subscribed',
            'recipes',
            'recipes_count',
        )

    def get_is_subscribed(self, obj):
        request = self.context.get('request')
        if not request or request.user.is_anonymous:
            return False
        return request.user.follower.filter(author=obj).exists()

    def get_recipes(self, obj):
        request = self.context.get('request')
        if request.user.is_anonymous:
            return False
        context = {request: request}
        recipes_limit = request.query_params.get('recipes_limit')
        if recipes_limit is not None:
            recipes = obj.recipes.all()[:int(recipes_limit)]
        else:
            recipes = obj.recipes.all()
        return FollowRecipeSerializer(recipes, many=True, context=context).data

    @staticmethod
    def get_recipes_count(obj):
        return obj.recipes.count()


class ShoppingCartSerializer(serializers.ModelSerializer):
    class Meta:
        model = ShoppingCart
        fields = ('user', 'recipe')

    def validate(self, data):
        request = self.context.get('request')
        if not request or request.user.is_anonymous:
            return False
        recipe = data['recipe']
        if request.user.shopping_cart_user.filter(recipe=recipe).exists():
            raise serializers.ValidationError(settings.RECIPE_IN_CART_ERROR)
        return data

    def to_representation(self, instance):
        request = self.context.get('request')
        context = {'request': request}
        return RecipeViewSerializer(
            instance.recipe,
            context=context
        ).data
