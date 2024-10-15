from django.shortcuts import render

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
    return render(request, 'consultas.html')

def medicos(request):
    return render(request, 'medicos.html')