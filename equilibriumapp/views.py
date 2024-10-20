from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.password_validation import validate_password
from .validators.validators import *
from .models import *

def homepage(request):
    return render(request, 'homepage.html')

def fazer_login(request):
    if request.method == 'POST':
        dados = request.POST.dict()
        print(dados)
        email = dados.get('email')
        senha = dados.get('senha')
        usuario = authenticate(username=email, password=senha)
        if usuario is not None:
            print("Usuário autenticado com sucesso")
            login(request,usuario)
            messages.success(request, 'Login realizado com sucesso')
            return redirect('homepage')
        else:
            print("Erro ao autenticar usuário")
            messages.error(request,'Email ou senha incorretos')

    return render(request, 'formularios/login.html')

def criar_conta(request):
    if request.method == 'POST':
        dados = request.POST.dict()
        nome = dados.get('nome')
        email = dados.get('email')
        cpf = dados.get('cpf')
        senha = dados.get('senha')
        role = dados.get('role')
        
        try:
            # Validações personalizadas
            validar_nome_completo(nome)
            validar_email(email)
            validar_cpf(cpf)
            validate_password(senha)
            
            # Verifica se o email já existe
            if User.objects.filter(username=email).exists():
                messages.error(request, "E-mail já existente.")
                return redirect('criar_conta')
            
            if Medico.objects.filter(cpf=cpf).exists() or Paciente.objects.filter(cpf=cpf).exists():
                messages.error(request, "CPF já registrado.")
                return redirect('criar_conta')

            # Lógica para Terapeuta
            if role == 'Terapeuta':
                medico_existente = Medico.objects.filter(email=email).exists()
                if medico_existente:
                    messages.error(request, "Médico já existente.")
                    return redirect('criar_conta')
                else:
                    medico = Medico.objects.create(nome=nome, email=email, cpf=cpf)
                    medico.save()
                    usuario_medico = User.objects.create_user(username=email, password=senha)
                    usuario_medico.save()

                    # Autentica e loga o médico
                    usuario = authenticate(username=email, password=senha)
                    login(request, usuario)
                    messages.success(request, 'Conta de Terapeuta criada com sucesso')
                    return redirect('homepage')

            # Lógica para Paciente
            elif role == 'Paciente':
                paciente_existente = Paciente.objects.filter(email=email).exists()
                if paciente_existente:
                    messages.error(request, "Paciente já existente.")
                    return redirect('criar_conta')
                else:
                    paciente = Paciente.objects.create(nome=nome, email=email, cpf=cpf)
                    usuario_paciente = User.objects.create_user(username=email, password=senha)
                    paciente.save()
                    usuario_paciente.save()

                    # Autentica e loga o paciente
                    usuario = authenticate(username=email, password=senha)
                    login(request, usuario)
                    messages.success(request, 'Conta de Paciente criada com sucesso')
                    return redirect('homepage')

            else:
                messages.error(request, 'Papel inválido.')
                return redirect('criar_conta')

        except ValidationError as e:
            for error in e:
                messages.error(request, error)

    return render(request, 'formularios/criar_conta.html')


@login_required
def fazer_logout(request):
    logout(request)
    return redirect('fazer_login')

@login_required
def dashboard(request):
    return render(request, 'dashboard.html')

@login_required
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