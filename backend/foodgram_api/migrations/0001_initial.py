# Generated by Django 3.2.7 on 2021-09-25 08:50

import django.core.validators
import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Ingredient',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('measurement_unit', models.CharField(max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='Portions',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.IntegerField()),
                ('ingredient', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='foodgram_api.ingredient')),
            ],
        ),
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('color', models.CharField(max_length=7, null=True)),
                ('slug', models.SlugField(max_length=200, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Recipe',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('image', models.URLField()),
                ('text', models.TextField()),
                ('cooking_time', models.IntegerField(validators=[django.core.validators.MinValueValidator(1)])),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('ingredients', models.ManyToManyField(through='foodgram_api.Portions', to='foodgram_api.Ingredient')),
                ('tags', models.ManyToManyField(to='foodgram_api.Tag')),
            ],
        ),
        migrations.AddField(
            model_name='portions',
            name='recipe',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='foodgram_api.recipe'),
        ),
    ]
