import csv

from django.core.management.base import BaseCommand
from django.db import IntegrityError

from recipes.models import Ingredient, Tag


class Command(BaseCommand):

    def handle(self, *args, **options):
        ingredients_to_create = []
        ingredients_to_check = set()
        with open(
                'recipes/data/ingredients.csv', 'r',
                encoding='utf-8'
        ) as file:
            file_reader = csv.reader(file)
            for row in file_reader:
                name, measurement_unit = row
                if name in ingredients_to_check:
                    continue
                ingredients_to_check.add(name)
                ingredient = Ingredient(
                    name=name, measurement_unit=measurement_unit
                )
                ingredients_to_create.append(ingredient)
            try:
                Ingredient.objects.bulk_create(ingredients_to_create)
            except IntegrityError as error:
                print(f'Возникла ошибка при добавлении ингредиентов: {error}')
        tags_to_create = []
        tags_to_check = set()
        with open('recipes/data/tags.csv', 'r', encoding='utf-8') as file:
            file_reader = csv.reader((file))
            for row in file_reader:
                name, color, slug = row
                if name in tags_to_check:
                    continue
                tag = Tag(name=name, color=color, slug=slug)
                tags_to_create.append(tag)
            try:
                Tag.objects.bulk_create(tags_to_create)
            except IntegrityError as error:
                print(f'Возникла ошибка при добавлении тегов: {error}')
