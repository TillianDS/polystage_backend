# Generated by Django 5.0.6 on 2024-07-14 09:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('back', '0058_session_nom_filiere'),
    ]

    operations = [
        migrations.AddConstraint(
            model_name='jury',
            constraint=models.UniqueConstraint(fields=('num_jury', 'session'), name='num_jury_session'),
        ),
    ]