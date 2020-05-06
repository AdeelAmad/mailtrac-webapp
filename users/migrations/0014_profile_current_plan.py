# Generated by Django 2.2.1 on 2020-04-03 21:03

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('payments', '0009_auto_20200403_1355'),
        ('users', '0013_remove_profile_current_plan'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='current_plan',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.PROTECT, to='payments.membership'),
        ),
    ]
