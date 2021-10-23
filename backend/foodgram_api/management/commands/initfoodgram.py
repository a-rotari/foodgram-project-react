import json

from django.core.management.base import BaseCommand, CommandError

from foodgram_api.models import Ingredient, Tag
from users_api.models import User


class Command(BaseCommand):
    help = 'Initializes the foodgram database and creates admin user'

    def handle(self, *arga, **options):
        i = Ingredient.objects.all()
        t = Tag.objects.all()

        if not i:
            with open('ingredients.json', encoding='utf-8') as data_file:
                json_data = json.loads(data_file.read())

                for ingredient_data in json_data:
                    Ingredient.objects.create(**ingredient_data)

        if not t:
            with open('tags.json', encoding='utf-8') as data_file:
                json_data = json.loads(data_file.read())

                for tag_data in json_data:
                    Tag.objects.create(**tag_data)
