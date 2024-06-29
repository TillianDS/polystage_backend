# Generated by Django 5.0.6 on 2024-06-28 19:10

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('back', '0042_remove_filiere_nom_directeur_and_more'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Enseignant',
            new_name='MembreJury',
        ),
        migrations.RemoveField(
            model_name='jury',
            name='professionnel',
        ),
        migrations.AlterModelOptions(
            name='membrejury',
            options={'verbose_name': 'user', 'verbose_name_plural': 'users'},
        ),
        migrations.RenameField(
            model_name='jury',
            old_name='enseignant',
            new_name='membreJury',
        ),
        migrations.DeleteModel(
            name='Professionnel',
        ),
    ]