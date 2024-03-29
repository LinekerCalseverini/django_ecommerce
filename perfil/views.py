'''
Módulo para definição das views do app Perfil.
'''
# pylint: disable=E1101,W0201, W0613
from typing import Any
import copy
from django.http.request import HttpRequest
from django.shortcuts import render, get_object_or_404, redirect
from django.views import View
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages


from .models import Perfil
from .forms import UserForm, PerfilForm

# Create your views here.


class BasePerfil(View):
    '''
    View para definir como renderizar o formulário de atualização de dados ou
    criação do perfil.
    '''
    template_name = 'perfil/criar.html'

    def setup(self, request: HttpRequest, *args: Any, **kwargs: Any) -> None:
        super().setup(request, *args, **kwargs)
        self.carrinho = copy.deepcopy(self.request.session.get('carrinho', {}))

        self.perfil = None
        if self.request.user.is_authenticated:
            self.template_name = 'perfil/atualizar.html'
            self.perfil = (Perfil.objects.filter(usuario=self.request.user)
                           .first())
            self.contexto = {
                'userform': UserForm(data=self.request.POST or None,
                                     usuario=self.request.user,
                                     instance=self.request.user),
                'perfilform': PerfilForm(data=self.request.POST or None,
                                         instance=self.perfil),
                'page_title': 'Atualizar Dados - '
            }
        else:
            self.contexto = {
                'userform': UserForm(data=self.request.POST or None),
                'perfilform': PerfilForm(data=self.request.POST or None),
                'page_title': 'Conectar - '
            }

        self.renderizar = render(
            self.request, self.template_name, self.contexto
        )

    def get(self, *args, **kwargs):
        '''
        Método que define como a View responderá a requisições de GET.
        '''
        return self.renderizar


class Criar(BasePerfil):
    '''
    Função de Definição de como o formulário de cadastro será renderizado.
    '''

    def post(self, *args, **kwargs):
        '''
        Método que define como a View responderá a requisições de POST.
        '''
        userform = self.contexto['userform']
        perfilform = self.contexto['perfilform']

        if not userform.is_valid() or not perfilform.is_valid():
            messages.error(
                self.request,
                'Alguns campos estão com erro. Revise seus dados.'
            )
            return self.renderizar

        password = userform.cleaned_data.get('password')

        # Usuário logado
        if self.request.user.is_authenticated:
            username = userform.cleaned_data.get('username')
            email = userform.cleaned_data.get('email')
            first_name = userform.cleaned_data.get('first_name')
            last_name = userform.cleaned_data.get('last_name')
            usuario = get_object_or_404(User, pk=self.request.user.pk)
            usuario.username = username
            usuario.email = email
            usuario.first_name = first_name
            usuario.last_name = last_name

        # Usuário não logado (novo)
        else:
            usuario = userform.save(commit=False)

        if password:
            usuario.set_password(password)

        usuario.save()

        perfil = perfilform.save(commit=False)
        perfil.usuario = usuario
        perfil.save()

        if password:
            autentica = authenticate(
                self.request,
                username=usuario,
                password=password
            )

            if autentica:
                login(self.request, user=usuario)

        self.request.session['carrinho'] = self.carrinho
        self.request.session.save()

        messages.success(
            self.request,
            'Dados atualizados.'
        )

        return redirect('produto:carrinho')


class Login(View):
    '''
    View que define como o login será autenticado.
    '''

    def post(self, *args, **kwargs):
        '''
        Como essa função exige que o usuário mande dados para que possa se
        logar, esta classe só aceita requisições POST.
        '''
        username = self.request.POST.get('username')
        password = self.request.POST.get('password')

        if not username or not password:
            messages.error(
                self.request,
                'Usuário ou senha não preenchidos.'
            )
            return redirect('perfil:criar')

        usuario = authenticate(
            self.request,
            username=username,
            password=password
        )

        if not usuario:
            messages.error(
                self.request,
                'Usuário ou senha inválidos.'
            )
            return redirect('perfil:criar')

        login(self.request, user=usuario)
        messages.success(
            self.request,
            'Conectado com sucesso.'
        )
        return redirect('produto:carrinho')


class Logout(View):
    '''
    View que define como o usuário se deslogará do sistema.
    '''

    def get(self, *args, **kwargs):
        '''
        Essa view pode usar requisições GET, já que só exige uma sessão
        autenticada.
        '''
        carrinho = copy.deepcopy(self.request.session.get('carrinho', {}))
        logout(self.request)
        self.request.session['carrinho'] = carrinho
        self.request.session.save()
        return redirect('produto:lista')
