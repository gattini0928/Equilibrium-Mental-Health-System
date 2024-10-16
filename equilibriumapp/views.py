from django.shortcuts import render
from .models import *

def homepage(request):
    context = {'Mo':'Teste'}
    return render(request, 'homepage.html', context)

def fazer_login(request):
    return render(request, 'formularios/login.html')

def criar_conta(request):
    return render(request, 'formularios/criar_conta.html')

def dashboard(request):
    return render(request, 'dashboard.html')

def consulta(request):
    return render(request, 'consulta.html')

def medicos(request):
    medicos = Medico.objects.all()
    horarios = Horarios.objects.filter(ocupado=False, 
                                       horario_inicio__gte=time(9,30), 
                                       horario_fim__lte=time(19,0))
    context = {'medicos':medicos, 'horarios':horarios}
    return render(request, 'medicos.html', context)

def biblioteca(request):
    return render(request, 'biblioteca.html')