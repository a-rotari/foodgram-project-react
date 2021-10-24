# Generated by Django 3.2.7 on 2021-10-24 18:57

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('foodgram_api', '0016_alter_portion_unique_together'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='favorite',
            options={'verbose_name': "User's favorite Recipe", 'verbose_name_plural': "Users' favorite Recipes"},
        ),
        migrations.AlterModelOptions(
            name='ingredient',
            options={'verbose_name': 'Ingredient', 'verbose_name_plural': 'Ingredients'},
        ),
        migrations.AlterModelOptions(
            name='portion',
            options={'verbose_name': 'Ingredient in a Recipe', 'verbose_name_plural': 'Ingredients in Recipes'},
        ),
        migrations.AlterModelOptions(
            name='recipe',
            options={'verbose_name': 'Recipe', 'verbose_name_plural': 'Recipes'},
        ),
        migrations.AlterModelOptions(
            name='shoppingcart',
            options={'verbose_name': 'Recipe in Shopping Cart', 'verbose_name_plural': 'Recipes in Shopping Carts'},
        ),
        migrations.AlterModelOptions(
            name='tag',
            options={'verbose_name': 'Tag', 'verbose_name_plural': 'Tags'},
        ),
    ]
