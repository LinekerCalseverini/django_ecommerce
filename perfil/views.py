from typing import Any
from django.http.request import HttpRequest
from django.shortcuts import render, get_object_or_404
from django.views import View
from django.http import HttpResponse
from django.contrib.auth.models import User

import copy

from .models import Perfil
from .forms import UserForm, PerfilForm

# Create your views here.


class BasePerfil(View):
    template_name = 'perfil/criar.html'

    def setup(self, request: HttpRequest, *args: Any, **kwargs: Any) -> None:
        super().setup(request, *args, **kwargs)
        self.carrinho = copy.deepcopy(self.request.session.get('carrinho', {}))

        self.perfil = None
        if self.request.user.is_authenticated:
            self.perfil = (Perfil.objects.filter(usuario=self.request.user)
                           .first())
            self.contexto = {
                'userform': UserForm(data=self.request.POST or None,
                                     usuario=self.request.user,
                                     instance=self.request.user),
                'perfilform': PerfilForm(data=self.request.POST or None,
                                         instance=self.perfil)
            }
        else:
            self.contexto = {
                'userform': UserForm(data=self.request.POST or None),
                'perfilform': PerfilForm(data=self.request.POST or None)
            }

        self.renderizar = render(
            self.request, self.template_name, self.contexto
        )

    def get(self, *args, **kwargs):
        return self.renderizar


class Criar(BasePerfil):
    def post(self, *args, **kwargs):
        userform = self.contexto['userform']
        perfilform = self.contexto['perfilform']

        if not userform.is_valid() or not perfilform.is_valid():
            return self.renderizar

        username = userform.cleaned_data.get('username')
        password = userform.cleaned_data.get('password')
        email = userform.cleaned_data.get('email')
        first_name = userform.cleaned_data.get('first_name')
        last_name = userform.cleaned_data.get('last_name')

        # Usuário logado
        if self.request.user.is_authenticated:
            usuario = get_object_or_404(User, pk=self.request.user.pk)
            usuario.username = username
            usuario.email = email

            if password:
                usuario.set_password(password)

            if first_name:
                usuario.first_name = first_name

            if last_name:
                usuario.last_name = last_name

            usuario.save()

        # Usuário não logado (novo)
        else:
            usuario = userform.save(commit=False)
            usuario.set_password(password)
            usuario.save()

            perfil = perfilform.save(commit=False)
            perfil.usuario = usuario
            perfil.save()

        self.request.session['carrinho'] = self.carrinho
        self.request.session.save()
        return self.renderizar


class Atualizar(BasePerfil):
    pass


class Login(View):
    def get(self, *args, **kwargs):
        return HttpResponse('Login')


class Logout(View):
    def get(self, *args, **kwargs):
        return HttpResponse('Logout')
