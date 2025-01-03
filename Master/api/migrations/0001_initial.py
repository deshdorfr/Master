# Generated by Django 5.1.2 on 2024-10-28 13:12

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='ESP32Device',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='Channel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('command', models.CharField(default='OFF', max_length=10)),
                ('esp_device', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='channels', to='api.esp32device')),
            ],
            options={
                'unique_together': {('esp_device', 'name')},
            },
        ),
    ]
