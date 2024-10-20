# Generated by Django 5.1.2 on 2024-10-17 18:56

import equilibriumapp.validators.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('equilibriumapp', '0008_alter_medico_usuario_alter_paciente_usuario'),
    ]

    operations = [
        migrations.AlterField(
            model_name='medico',
            name='cpf',
            field=models.CharField(default='00000000000', max_length=15, validators=[equilibriumapp.validators.validators.validar_cpf]),
        ),
        migrations.AlterField(
            model_name='medico',
            name='email',
            field=models.EmailField(max_length=200, validators=[equilibriumapp.validators.validators.validar_email]),
        ),
        migrations.AlterField(
            model_name='medico',
            name='nome',
            field=models.CharField(max_length=100, validators=[equilibriumapp.validators.validators.validar_nome_completo]),
        ),
        migrations.AlterField(
            model_name='paciente',
            name='cpf',
            field=models.CharField(default='00000000000', max_length=15, validators=[equilibriumapp.validators.validators.validar_cpf]),
        ),
        migrations.AlterField(
            model_name='paciente',
            name='email',
            field=models.EmailField(max_length=200, validators=[equilibriumapp.validators.validators.validar_email]),
        ),
        migrations.AlterField(
            model_name='paciente',
            name='nome',
            field=models.CharField(max_length=100, validators=[equilibriumapp.validators.validators.validar_nome_completo]),
        ),
    ]