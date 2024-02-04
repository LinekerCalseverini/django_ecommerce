# pylint: disable=E1101
'''
Módulo dos models do app Perfil
'''
from django.db import models
from django.contrib.auth.models import User
from django.forms import ValidationError

from utils.validacpf import valida_cpf

# Create your models here.


class Perfil(models.Model):
    '''
    Classe para Perfis de Usuário no Site
    '''
    class Meta:  # pylint: disable=C0115,R0903
        verbose_name = 'Perfil'
        verbose_name_plural = 'Perfis'

    usuario = models.OneToOneField(User, on_delete=models.CASCADE,
                                   verbose_name='Usuário')
    idade = models.PositiveIntegerField()
    data_nascimento = models.DateField(verbose_name='Data de Nascimento')
    cpf = models.CharField(max_length=11, verbose_name='CPF')
    endereco = models.CharField(max_length=50, verbose_name='Endereço')
    numero = models.CharField(max_length=5, verbose_name='Número')
    complemento = models.CharField(default='', max_length=30)
    bairro = models.CharField(max_length=30)
    cep = models.CharField(max_length=8, verbose_name='CEP')
    cidade = models.CharField(max_length=30)
    estado = models.CharField(
        default='SP',
        max_length=2,
        choices=(
            ('AC', 'Acre'),
            ('AL', 'Alagoas'),
            ('AP', 'Amapá'),
            ('AM', 'Amazonas'),
            ('BA', 'Bahia'),
            ('CE', 'Ceará'),
            ('DF', 'Distrito Federal'),
            ('ES', 'Espírito Santo'),
            ('GO', 'Goiás'),
            ('MA', 'Maranhão'),
            ('MT', 'Mato Grosso'),
            ('MS', 'Mato Grosso do Sul'),
            ('MG', 'Minas Gerais'),
            ('PA', 'Pará'),
            ('PB', 'Paraíba'),
            ('PR', 'Paraná'),
            ('PE', 'Pernambuco'),
            ('PI', 'Piauí'),
            ('RJ', 'Rio de Janeiro'),
            ('RN', 'Rio Grande do Norte'),
            ('RS', 'Rio Grande do Sul'),
            ('RO', 'Rondônia'),
            ('RR', 'Roraima'),
            ('SC', 'Santa Catarina'),
            ('SP', 'São Paulo'),
            ('SE', 'Sergipe'),
            ('TO', 'Tocantins'),
        )
    )

    def __str__(self) -> str:
        if not self.usuario.first_name:  # pylint: disable=E1101
            return self.usuario.username  # pylint: disable=E1101

        # pylint: disable-next=E1101
        return f'{self.usuario.first_name} {self.usuario.last_name}'

    def clean(self):
        error_messages = {}

        cpf_enviado = self.cpf or None
        perfil = Perfil.objects.filter(cpf=cpf_enviado).first()

        if not valida_cpf(self.cpf):
            error_messages['cpf'] = 'CPF Inválido'

        if perfil and (perfil.pk != self.pk or not self.pk):
            error_messages['cpf'] = 'CPF já está sendo utilizado'

        # pylint: disable-next=E1101
        if not self.cep.isnumeric() or len(self.cep) != 8:
            error_messages['cep'] = 'CEP deve ser um valor de 8 dígitos'

        if error_messages:
            raise ValidationError(error_messages)
