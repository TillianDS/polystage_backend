# Generated by Django 5.0.6 on 2024-06-29 08:32

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('back', '0044_enseignant_professionnel'),
        ('formulaire', '0009_formulaire_langue_alter_formulaire_profile'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='response',
            name='user',
        ),
        migrations.AddField(
            model_name='response',
            name='id_etudiant',
            field=models.ForeignKey(default=38, on_delete=django.db.models.deletion.CASCADE, related_name='etudiant', to='back.etudiant'),
            preserve_default=False,
        ),
    ]