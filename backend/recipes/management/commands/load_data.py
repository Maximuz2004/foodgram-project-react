import csv

from django.core.management.base import BaseCommand
from django.db import IntegrityError

from recipes.models import Ingredient, Tag


class Command(BaseCommand):

    def handle(self, *args, **options):
        ingredients_to_create = set()
        with open(
                'recipes/data/ingredients.csv', 'r',
                encoding='utf-8'
        ) as file:
            file_reader = csv.reader(file)
            for row in file_reader:
                name, measurement_unit = row
                ingredient = Ingredient(
                    name=name, measurement_unit=measurement_unit
                )
                ingredients_to_create.add(ingredient)
            try:
                Ingredient.objects.bulk_create(list(ingredients_to_create))
            except IntegrityError as error:
                print(f'Возникла ошибка при добавлении ингредиентов: {error}')
        tags_to_create = set()
        with open('recipes/data/tags.csv', 'r', encoding='utf-8') as file:
            file_reader = csv.reader((file))
            for row in file_reader:
                name, color, slug = row
                tag = Tag(name=name, color=color, slug=slug)
                tags_to_create.add(tag)
            try:
                Tag.objects.bulk_create(list(tags_to_create))
            except IntegrityError as error:
                print(f'Возникла ошибка при добавлении тегов: {error}')
