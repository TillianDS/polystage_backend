# Generated by Django 5.0.5 on 2024-05-16 15:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('back', '0013_soutenance_heure_soutenance'),
    ]

    operations = [
        migrations.AlterField(
            model_name='soutenance',
            name='heure_soutenance',
            field=models.TimeField(default=None),
        ),
    ]