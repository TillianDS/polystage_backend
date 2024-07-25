# Generated by Django 5.0.6 on 2024-07-25 13:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('back', '0064_codepassword_creation_date'),
    ]

    operations = [
        migrations.AddField(
            model_name='session',
            name='status',
            field=models.IntegerField(choices=[(1, 'cachée'), (2, 'ouverte'), (3, 'terminée')], default=1),
        ),
    ]
