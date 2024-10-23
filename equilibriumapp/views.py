from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group
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
                    usuario_medico = User.objects.create_user(username=email, password=senha)
                    usuario_medico.save()
                    grupo_medicos = Group.objects.get(name='medicos')  # Certifique-se de que o grupo existe
                    usuario_medico.groups.add(grupo_medicos)  # Adiciona o usuário ao grupo
                    medico = Medico.objects.create(nome=nome, email=email, cpf=cpf)
                    medico.save()

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

    if not hasattr(request.user, 'medico'):
        messages.error(request, 'Você precisa ser um médico para acessar esta página.')
        return redirect('homepage')  # Redireciona para a homepage ou outra página que desejar

    medico = get_object_or_404(Medico, usuario=request.user)
    pacientes = medico.pacientes.all()

    horarios_ocupados = Horarios.objects.filter(medico=medico, ocupado=True)
    horarios_disponiveis = Horarios.objects.filter(medico=medico, ocupado=False)

    context = {
        'medico':medico,
        'pacientes':pacientes,
        'horarios_ocupados':horarios_ocupados,
        'horarios_disponiveis':horarios_disponiveis
    }

    return render(request, 'dashboard.html', context)

@login_required
def agendar_consulta(request, horario_id):
    
    medico = get_object_or_404(Medico, usuario=request.user)
    horario = get_object_or_404(Horarios, medico=medico , id=horario_id)

    if request.method == 'POST':
        horario.ocupado = True
        horario.save()
        return redirect('dashboard')

@login_required
def remarcar_consulta(request, horario_id):
    medico = get_object_or_404(Medico, usuario=request.user)
    horario = get_object_or_404(Horarios, medico=medico, id=horario_id)

    if request.method == 'POST':
        horario.ocupado = False
        horario.save()
        return redirect('dashboard')


def remover_paciente(request, paciente_id):
    medico = get_object_or_404(Medico, usuario=request.user)
    paciente = get_object_or_404(Paciente, medicos=medico, id=paciente_id)
    if request.method == 'POST':
        medico.remover_paciente(paciente)
        messages.success(request,f'Paciente {paciente.nome} foi removido')
        return redirect('dashboard')
    return render(request,'dashboard.html')

def pacientes(request, paciente_id=None):
    medico = get_object_or_404(Medico, usuario=request.user)
    pacientes = Paciente.objects.filter(medicos=medico)
    paciente = None
    if paciente_id:
        paciente = get_object_or_404(pacientes, id=paciente_id)

    context = {'pacientes':pacientes, 'paciente':paciente}
    return render(request, 'pacientes.html', context)
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