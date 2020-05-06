# Generated by Django 2.2.1 on 2020-01-11 01:18

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='tracker',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=150)),
                ('description', models.TextField()),
                ('tracking_number', models.CharField(max_length=50)),
                ('carrier', models.CharField(choices=[('USPS', 'USPS'), ('FedEx', 'FedEx'), ('UPS', 'UPS'), ('Other', 'Other')], max_length=8)),
            ],
        ),
    ]
