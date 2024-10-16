from django.db import models
from django.contrib.auth.models import User
from datetime import time
from django.core.exceptions import ValidationError

class Medico(models.Model):
    nome = models.CharField(max_length=100, null=False, blank=False)
    email = models.EmailField(max_length=200, null=False, blank=False)
    usuario = models.OneToOneField(User, null=False, blank=False, on_delete=models.CASCADE)
    cpf = models.CharField(max_length=15, null=False, blank=False, default="00000000000")
    def __str__(self):
        return self.nome
    def agendar_consulta(self,medico, horario_inicio,horario_fim, dia_semana):
        try:
            horario = Horarios.objects.get(medico=medico,
                                    horario_inicio=horario_inicio, 
                                    horario_fim=horario_fim, 
                                    dia_semana=dia_semana)
            if horario.ocupado:
                raise ValidationError('Esse horário já está ocupado.')
            horario.ocupado = True
            horario.save()
        except Horarios.DoesNotExist:
            raise ValidationError('Este horário não existe')

    def desmarcar_consulta(self, medico, dia_semana, horario_inicio, horario_fim):
        try:
            horario = Horarios.objects.get(dia_semana=dia_semana, 
                                           medico=medico, 
                                           horario_inicio=horario_inicio,
                                         horario_fim=horario_fim)
            horario.ocupado = False
            horario.save()
        except Horarios.DoesNotExist:
            raise ValidationError('Este horário não existe')
class Horarios(models.Model):
    medico = models.ForeignKey(Medico, on_delete=models.CASCADE, related_name='horarios')
    dia_semana = models.CharField(max_length=15, choices=[
        ('Segunda', 'Segunda-feira'),
        ('Terça', 'Terça-feira'),
        ('Quarta', 'Quarta-feira'),
        ('Quinta', 'Quinta-feira'),
        ('Sexta', 'Sexta-feira'),
        ('Sábado', 'Sábado'),
        ('Domingo', 'Domingo'),
    ])
    horario_inicio = models.TimeField()
    horario_fim = models.TimeField()
    ocupado = models.BooleanField(default=False)

    def clean(self):
        if self.horario_inicio is None or self.horario_fim is None:
            raise ValidationError('Horário de início e fim são obrigatórios.')
        # Limitação de horário entre 07:00 e 19:00
        if not (time(7, 0) <= self.horario_inicio <= time(19, 0)):
            raise ValidationError('O horário de inicio estar entre 07:00 e 19:00.')
        if not (time(7, 0) <= self.horario_fim <= time(19, 0)):
            raise ValidationError('O horário de fim deve estar entre 07:00 e 19:00.')
        if self.horario_inicio >= self.horario_fim:
            raise ValidationError('O horário de início deve ser anterior ao horário de fim.')

    def __str__(self):
        return f'{self.dia_semana}: {self.horario_inicio} - {self.horario_fim} ({self.medico.nome}) - {"Ocupado" if self.ocupado else "Disponível"}'


class Paciente(models.Model):
    nome = models.CharField(max_length=100, null=False, blank=False)
    medicos = models.ManyToManyField(Medico, blank=True, related_name='pacientes')
    email = models.EmailField(max_length=200, null=False, blank=False)
    cpf = models.CharField(max_length=15, null=False, blank=False, default="00000000000")

    def marcar_consulta(self, dia_semana, horario_inicio, horario_fim, medico):
        medico = Medico.objects.get(pk=medico.pk)
        if medico:
                try:
                    horario = Horarios.objects.get(
                        medico=medico,
                        ocupado=False,
                        dia_semana=dia_semana, 
                        horario_inicio=horario_inicio,
                        horario_fim=horario_fim)
                    horario.ocupado = True
                    horario.save()
                    return f"Consulta marcada com o médico {medico.nome} no horário {horario_inicio} - {horario_fim} ({dia_semana})"
                except Horarios.DoesNotExist:
                    raise ValidationError('Este horário não está disponível ou não existe.')

    def __str__(self):
        return self.nome
    
