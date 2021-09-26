# Generated by Django 3.2.7 on 2021-09-25 09:51

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('foodgram_api', '0002_auto_20210925_0927'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tag',
            name='color',
            field=models.CharField(max_length=7, unique=True, validators=[django.core.validators.RegexValidator('#[0-9A-F]{6}$', "Color code must be in hex format, i.e. '#FFFFFF'")]),
        ),
    ]
