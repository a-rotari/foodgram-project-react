# Generated by Django 3.2.7 on 2021-09-25 15:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('foodgram_api', '0005_favorite'),
    ]

    operations = [
        migrations.AlterField(
            model_name='favorite',
            name='recipes',
            field=models.ManyToManyField(blank=True, to='foodgram_api.Recipe'),
        ),
    ]
