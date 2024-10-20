from django.core.exceptions import ValidationError
from validate_docbr import CPF
def validar_nome_completo(nome:str):
    if len(nome.split()) <= 1:
        raise ValidationError('Digite seu nome completo')
    return nome

def validar_email(email:str):
    domains = ['icloud.com' , 'gmail.com', 'outlook.com', 'yahoo.com']
    domain = email.split("@")[-1]
    if domain not in domains:
        raise ValidationError('Domínio de e-mail inválido. Use um domínio como gmail.com, outlook.com, etc.')
    return email

def validar_cpf(cpf):
    cpf_obj = CPF()
    if not cpf_obj.validate(cpf):
        raise ValidationError(f'Seu CPF {cpf} é inválido')
    return cpf
     