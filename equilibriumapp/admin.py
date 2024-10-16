from django.contrib import admin
from .models import Medico, Paciente, Horarios

# In-line para gerenciar horários diretamente no admin de Médico
class HorariosInline(admin.TabularInline):
    model = Horarios
    extra = 1

@admin.register(Medico)
class MedicoAdmin(admin.ModelAdmin):
    list_display = ('nome', 'email')
    inlines = [HorariosInline]

@admin.register(Paciente)
class PacienteAdmin(admin.ModelAdmin):
    list_display = ('nome', 'email')
    filter_horizontal = ('medicos',)  # Filtro horizontal para a relação ManyToMany de médicos

# Registro de Horarios diretamente no admin
admin.site.register(Horarios)


