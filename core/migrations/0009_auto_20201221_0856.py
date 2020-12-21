# Generated by Django 3.1.4 on 2020-12-21 11:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0008_auto_20201220_1938'),
    ]

    operations = [
        migrations.AddField(
            model_name='horarioagenda',
            name='confirmacao',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='horarioagenda',
            name='hora_atendimento',
            field=models.TimeField(blank=True, null=True),
        ),
    ]