import json
from foodgram_api.models import Ingredient, Tag

with open('ingredients.json', encoding='utf-8') as data_file:
    json_data = json.loads(data_file.read())

    for ingredient_data in json_data:
        Ingredient.objects.create(**ingredient_data)

with open('tags.json', encoding='utf-8') as data_file:
    json_data = json.loads(data_file.read())

    for tag_data in json_data:
        Tag.objects.create(**tag_data)
