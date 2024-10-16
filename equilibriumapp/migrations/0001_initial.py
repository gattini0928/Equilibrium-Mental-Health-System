# Generated by Django 5.1.2 on 2024-10-16 12:13

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Medico',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nome', models.CharField(max_length=100)),
                ('email', models.EmailField(max_length=200)),
                ('usuario', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Horarios',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('dia_semana', models.CharField(choices=[('Segunda', 'Segunda-feira'), ('Terça', 'Terça-feira'), ('Quarta', 'Quarta-feira'), ('Quinta', 'Quinta-feira'), ('Sexta', 'Sexta-feira'), ('Sábado', 'Sábado'), ('Domingo', 'Domingo')], max_length=15)),
                ('horario_inicio', models.TimeField()),
                ('horario_fim', models.TimeField()),
                ('ocupado', models.BooleanField(default=False)),
                ('medico', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='horarios', to='equilibriumapp.medico')),
            ],
        ),
    ]