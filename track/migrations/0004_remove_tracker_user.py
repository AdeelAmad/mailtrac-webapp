# Generated by Django 2.2.1 on 2020-01-11 01:48

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('track', '0003_tracker'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='tracker',
            name='user',
        ),
    ]