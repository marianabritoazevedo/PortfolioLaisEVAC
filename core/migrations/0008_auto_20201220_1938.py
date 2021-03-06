# Generated by Django 3.1.4 on 2020-12-20 22:38

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0007_agenda_fila_chamada'),
    ]

    operations = [
        migrations.AlterField(
            model_name='horarioagenda',
            name='agenda',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='core.agenda'),
        ),
        migrations.AlterField(
            model_name='horarioagenda',
            name='fila',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='horarioagenda',
            name='paciente',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='core.paciente'),
        ),
        migrations.AlterField(
            model_name='horarioagenda',
            name='vacina',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='core.vacina'),
        ),
    ]
