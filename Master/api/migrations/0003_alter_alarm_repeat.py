# Generated by Django 5.1.2 on 2024-11-11 11:48

import multiselectfield.db.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0002_alarm'),
    ]

    operations = [
        migrations.AlterField(
            model_name='alarm',
            name='repeat',
            field=multiselectfield.db.fields.MultiSelectField(choices=[('sunday', 'Sunday'), ('monday', 'Monday'), ('tuesday', 'Tuesday'), ('wednesday', 'Wednesday'), ('thursday', 'Thursday'), ('friday', 'Friday'), ('saturday', 'Saturday')], max_length=56),
        ),
    ]