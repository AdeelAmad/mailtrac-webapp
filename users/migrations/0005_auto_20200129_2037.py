# Generated by Django 2.2.1 on 2020-01-30 04:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0004_profile_phone'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='unlimited',
            field=models.BooleanField(default=True),
        ),
    ]
