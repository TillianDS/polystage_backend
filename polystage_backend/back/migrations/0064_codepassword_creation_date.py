# Generated by Django 5.0.6 on 2024-07-23 13:48

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('back', '0063_alter_soutenance_stage'),
    ]

    operations = [
        migrations.AddField(
            model_name='codepassword',
            name='creation_date',
            field=models.DateTimeField(default=datetime.datetime.now),
        ),
    ]
