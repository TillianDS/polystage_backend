# Generated by Django 5.0.6 on 2024-06-27 07:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('back', '0033_stage'),
    ]

    operations = [
        migrations.AlterField(
            model_name='stage',
            name='nom_entreprise',
            field=models.CharField(max_length=400),
        ),
    ]
