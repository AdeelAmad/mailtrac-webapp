# Generated by Django 2.2.1 on 2020-01-18 02:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('track', '0005_tracker_user'),
    ]

    operations = [
        migrations.AddField(
            model_name='tracker',
            name='sms',
            field=models.BooleanField(default=False),
        ),
    ]
