# Generated by Django 5.0.6 on 2024-06-29 12:38

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('back', '0044_enseignant_professionnel'),
        ('formulaire', '0012_rename_title_checkbox_titre_and_more'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Response',
            new_name='ResponseForm',
        ),
    ]
