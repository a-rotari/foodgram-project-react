# Generated by Django 3.2.7 on 2021-10-23 19:45

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users_api', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='usersubscription',
            options={'ordering': ['subscriber'], 'verbose_name': 'User Subscription', 'verbose_name_plural': 'User Subscriptions'},
        ),
    ]
