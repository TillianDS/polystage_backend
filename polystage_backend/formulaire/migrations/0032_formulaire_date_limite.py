# Generated by Django 5.0.6 on 2024-07-24 09:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('formulaire', '0031_remove_responseform_question_session_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='formulaire',
            name='date_limite',
            field=models.DateTimeField(null=True),
        ),
    ]
