# Generated by Django 3.2.7 on 2021-10-24 20:26

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('foodgram_api', '0019_merge_20211024_2202'),
    ]

    operations = [
        migrations.AlterField(
            model_name='portion',
            name='amount',
            field=models.IntegerField(validators=[django.core.validators.MinValueValidator(0, message='Количество ингредиентов не может быть отрицательным.')]),
        ),
    ]