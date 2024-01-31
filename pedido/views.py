from django.shortcuts import render, redirect
from django.views import View
from django.http import HttpResponse
from django.contrib import messages

from perfil.models import Perfil
from produto.models import Variacao
from produto.utils import formata_carrinho

from .models import Pedido, ItemPedido

# Create your views here.


class Pagar(View):
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
            print(estoque)
            qtd_carrinho = carrinho.get(vid, 0)

            if qtd_carrinho > estoque:
                qtd_carrinho = estoque
                carrinho_modificado = True

            carrinho[vid] = qtd_carrinho
            if qtd_carrinho == 0:
                carrinho.pop(vid, None)

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
        return redirect('pedido:lista')


class SalvarPedido(View):
    def get(self, *args, **kwargs):
        return HttpResponse('FecharPedido')


class Detalhe(View):
    def get(self, *args, **kwargs):
        return HttpResponse('Detalhe')


class ListaPedido(View):
    def get(self, *args, **kwargs):
        return HttpResponse('ListaPedido')
