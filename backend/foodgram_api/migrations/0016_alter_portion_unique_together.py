# Generated by Django 3.2.7 on 2021-10-24 14:10

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('foodgram_api', '0015_alter_recipe_cooking_time'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='portion',
            unique_together={('recipe', 'ingredient')},
        ),
    ]