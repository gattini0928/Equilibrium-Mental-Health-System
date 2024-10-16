# Generated by Django 5.1.2 on 2024-10-16 18:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('equilibriumapp', '0003_medico_cpf_paciente_cpf_alter_paciente_medicos'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='paciente',
            name='medicos',
        ),
        migrations.AddField(
            model_name='paciente',
            name='medicos',
            field=models.ManyToManyField(blank=True, related_name='pacientes', to='equilibriumapp.medico'),
        ),
    ]
