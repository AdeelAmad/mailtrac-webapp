# Generated by Django 2.2.1 on 2020-01-18 04:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('payments', '0005_subscription_membership'),
    ]

    operations = [
        migrations.AlterField(
            model_name='membership',
            name='membership_type',
            field=models.CharField(choices=[('Basic', 'Basic'), ('Pro', 'Pro'), ('Unlimited', 'Unlimited')], default='Basic', max_length=10),
        ),
    ]