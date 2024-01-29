from typing import Any
from django.http.request import HttpRequest as HttpRequest
from django.shortcuts import render
from django.views import View
from django.http import HttpResponse

from .forms import UserForm, PerfilForm

# Create your views here.


class BasePerfil(View):
    template_name = 'perfil/criar.html'

    def setup(self, request: HttpRequest, *args: Any, **kwargs: Any) -> None:
        super().setup(request, *args, **kwargs)

        if self.request.user.is_authenticated:
            contexto = {
                'userform': UserForm(data=self.request.POST or None,
                                     usuario=self.request.user,
                                     instance=self.request.user),
                'perfilform': PerfilForm(data=self.request.POST or None)
            }
        else:
            contexto = {
                'userform': UserForm(data=self.request.POST or None),
                'perfilform': PerfilForm(data=self.request.POST or None)
            }

        self.renderizar = render(self.request, self.template_name, contexto)

    def get(self, *args, **kwargs):
        return self.renderizar


class Criar(BasePerfil):
    def post(self, *args, **kwargs):
        return self.renderizar


class Atualizar(BasePerfil):
    pass


class Login(View):
    def get(self, *args, **kwargs):
        return HttpResponse('Login')


class Logout(View):
    def get(self, *args, **kwargs):
        return HttpResponse('Logout')
