# Generated by Django 5.0.6 on 2024-06-27 07:41

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('back', '0032_delete_stage'),
    ]

    operations = [
        migrations.CreateModel(
            name='Stage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sujet', models.TextField()),
                ('confidentiel', models.BooleanField(default=False)),
                ('date_debut', models.DateField()),
                ('date_fin', models.DateField()),
                ('nom_entreprise', models.CharField(max_length=200)),
                ('etudiant', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='stage', to='back.etudiant')),
                ('tuteur', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='back.tuteur')),
            ],
        ),
    ]
