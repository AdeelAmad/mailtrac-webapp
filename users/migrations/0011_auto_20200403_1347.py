# Generated by Django 2.2.1 on 2020-04-03 20:47

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0010_auto_20200403_1346'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='current_plan',
            field=models.ForeignKey(default=0, on_delete=django.db.models.deletion.PROTECT, to='payments.membership'),
        ),
    ]
