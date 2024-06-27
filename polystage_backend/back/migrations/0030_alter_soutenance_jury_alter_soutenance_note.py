# Generated by Django 5.0.6 on 2024-06-26 19:48

import django.core.validators
import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('back', '0029_alter_soutenance_date_soutenance_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='soutenance',
            name='jury',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='back.jury'),
        ),
        migrations.AlterField(
            model_name='soutenance',
            name='note',
            field=models.FloatField(null=True, validators=[django.core.validators.MaxValueValidator(20.0)]),
        ),
    ]