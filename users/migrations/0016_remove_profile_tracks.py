# Generated by Django 2.2.1 on 2020-04-28 20:41

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0015_auto_20200409_1416'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='profile',
            name='tracks',
        ),
    ]
