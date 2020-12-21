# Generated by Django 3.1.4 on 2020-12-20 11:27

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('core', '0002_estabelecimento_municipio_paciente_profissional_uf'),
    ]

    operations = [
        migrations.CreateModel(
            name='Agenda',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('data', models.DateField(auto_now_add=True)),
                ('fila', models.IntegerField()),
            ],
        ),
        migrations.AddField(
            model_name='estabelecimento',
            name='municipio',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='core.municipio'),
        ),
        migrations.AddField(
            model_name='municipio',
            name='uf',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='core.uf'),
        ),
        migrations.AddField(
            model_name='paciente',
            name='user',
            field=models.OneToOneField(default=None, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='profissional',
            name='estabelecimento',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='core.estabelecimento'),
        ),
        migrations.AddField(
            model_name='profissional',
            name='user',
            field=models.OneToOneField(default=None, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.CreateModel(
            name='PacienteVacina',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('data', models.DateField(auto_now_add=True)),
                ('paciente', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='core.paciente')),
                ('vacina', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='core.vacina')),
            ],
        ),
        migrations.CreateModel(
            name='HorarioAgenda',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('horario', models.TimeField(blank=True, null=True)),
                ('hora_chegada', models.TimeField(blank=True, null=True)),
                ('hora_chamada', models.TimeField(blank=True, null=True)),
                ('fila', models.IntegerField()),
                ('agenda', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='core.agenda')),
                ('paciente', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='core.paciente')),
                ('vacina', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='core.vacina')),
            ],
        ),
        migrations.AddField(
            model_name='agenda',
            name='estabelecimento',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='core.estabelecimento'),
        ),
    ]