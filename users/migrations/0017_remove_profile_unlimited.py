# Generated by Django 2.2.1 on 2020-04-28 20:42

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0016_remove_profile_tracks'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='profile',
            name='unlimited',
        ),
    ]
