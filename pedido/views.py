from typing import Any
from django.db.models.query import QuerySet
from django.shortcuts import reverse, redirect
from django.views import View
from django.views.generic import DetailView, ListView
from django.http import HttpRequest, HttpResponse
from django.contrib import messages

from perfil.models import Perfil
from produto.models import Variacao
from produto.utils import formata_carrinho

from .models import Pedido, ItemPedido

# Create your views here.


class DispatchLoginRequiredMixin(View):
    def dispatch(self, *args, **kwargs):
        if not self.request.user.is_authenticated:
            return redirect('perfil:criar')

        return super().dispatch(*args, **kwargs)

    def get_queryset(self) -> QuerySet[Any]:
        return super().get_queryset().filter(usuario=self.request.user)


class Pagar(DispatchLoginRequiredMixin, DetailView):
    template_name = 'pedido/pagar.html'
    model = Pedido
    pk_url_kwarg = 'pk'
    context_object_name = 'pedido'

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        ctx = super().get_context_data(**kwargs)
        ctx.update({
            'page_title': f'{self.get_object()} - Pagar - '
        })
        return ctx


class SalvarPedido(View):
    template_name = 'pedido/pagar.html'

    def get(self, *args, **kwargs):
        usuario = self.request.user
        if not usuario.is_authenticated:
            return redirect('produto:lista')

        perfil = Perfil.objects.filter(usuario=usuario).exists()

        if not perfil:
            return redirect('perfil:criar')

        carrinho = self.request.session.get('carrinho')
        if not carrinho:
            return redirect('produto:lista')

        vids = list(carrinho)
        bd_variacoes = list(
            Variacao.objects.select_related('produto').filter(id__in=vids)
        )

        carrinho_modificado = False
        for variacao in bd_variacoes:
            vid = str(variacao.pk)
            estoque = variacao.estoque
            qtd_carrinho = carrinho.get(vid, 0)

            if qtd_carrinho > estoque:
                qtd_carrinho = estoque
                carrinho_modificado = True

            carrinho[vid] = qtd_carrinho
            if qtd_carrinho == 0:
                carrinho.pop(vid, None)

            estoque -= qtd_carrinho
            variacao.estoque = estoque
            variacao.save()

        self.request.session['carrinho'] = carrinho
        self.request.session.save()

        if carrinho_modificado:
            messages.warning(
                self.request,
                ('Alguns produtos diminuíram de estoque, alteramos o seu '
                    'carrinho. Revise sua compra.')
            )
            return redirect('produto:carrinho')

        carrinho_info = formata_carrinho(carrinho)

        total_pedido = sum(item['total'] for item in carrinho_info.values())
        total_itens = sum(value for value in carrinho.values())

        pedido = Pedido(
            usuario=self.request.user,
            total=total_pedido,
            qtd_total=total_itens,
            status='C'
        )
        pedido.save()

        ItemPedido.objects.bulk_create(
            [
                ItemPedido(
                    pedido=pedido,
                    variacao=item['variacao_obj'],
                    preco=item['preco'],
                    quantidade=item['quantidade']
                ) for item in carrinho_info.values()
            ]
        )

        self.request.session.pop('carrinho', None)
        self.request.session.save()

        return redirect(
            reverse(
                'pedido:pagar',
                kwargs={
                    'pk': pedido.pk
                }
            )
        )


class Detalhe(DispatchLoginRequiredMixin, DetailView):
    template_name = 'pedido/detalhe.html'
    model = Pedido
    pk_url_kwarg = 'pk'
    context_object_name = 'pedido'

    def get(self, request, *args, **kwargs):
        pedido = self.get_object()
        if pedido.status in 'CRP':
            return redirect(
                reverse(
                    'pedido:pagar',
                    kwargs={
                        'pk': pedido.pk
                    }
                )
            )
        return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        ctx = super().get_context_data(**kwargs)
        ctx.update({
            'page_title': f'{self.get_object()} - Detalhe - '
        })
        return ctx


class ListaPedido(DispatchLoginRequiredMixin, ListView):
    model = Pedido
    context_object_name = 'pedidos'
    template_name = 'pedido/lista.html'
    paginate_by = 10
    ordering = ['-id']

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        ctx = super().get_context_data(**kwargs)
        usuario = Perfil.objects.filter(usuario=self.request.user).first()
        ctx.update({
            'usuario': usuario,
            'page_title': f'Pedidos de {usuario} - '
        })
        return ctx
