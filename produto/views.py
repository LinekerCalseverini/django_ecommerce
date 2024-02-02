from typing import Any
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views import View
from django.contrib import messages
from .models import Produto, Variacao
from .utils import formata_carrinho
from perfil.models import Perfil

# Create your views here.


class ListaProduto(ListView):
    model = Produto
    template_name = 'produto/lista.html'
    context_object_name = 'produtos'
    paginate_by = 12
    ordering = ['-id']

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        ctx = super().get_context_data(**kwargs)

        ctx.update({
            'page_title': 'Produtos - '
        })

        return ctx


class DetalheProduto(DetailView):
    model = Produto
    template_name = 'produto/detalhe.html'
    context_object_name = 'produto'
    slug_url_kwarg = 'slug'

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        ctx = super().get_context_data(**kwargs)
        produto = self.get_object()

        ctx.update({
            'page_title': f'Comprar {produto.nome} - '
        })

        return ctx


class AdicionarAoCarrinho(View):
    def get(self, *args, **kwargs):
        http_referer = self.request.META.get(
            'HTTP_REFERER',
            reverse('produto:lista')
        )
        variacao_id = self.request.GET.get('vid')

        if not variacao_id:
            messages.error(
                self.request,
                'Produto não existe.'
            )
            return redirect(http_referer)

        variacao = get_object_or_404(Variacao, id=variacao_id)
        carrinho = self.request.session.get('carrinho', {})

        quantidade = carrinho.get(variacao_id, 0)
        quantidade += 1
        if variacao.estoque < quantidade:
            messages.error(
                self.request,
                'Estoque insuficiente.'
            )
            return redirect(http_referer)

        carrinho[variacao_id] = quantidade
        self.request.session['carrinho'] = carrinho
        self.request.session.save()

        messages.success(
            self.request,
            'Produto adicionado com sucesso.'
        )

        return redirect(http_referer)


class RemoverDoCarrinho(View):
    def get(self, *args, **kwargs):
        http_referer = self.request.META.get(
            'HTTP_REFERER',
            reverse('produto:lista')
        )
        variacao_id = self.request.GET.get('vid')

        if not variacao_id:
            return redirect(http_referer)

        carrinho = self.request.session.get('carrinho', {})
        quantidade = carrinho.get(variacao_id)

        if not quantidade:
            return redirect(http_referer)

        carrinho.pop(variacao_id, None)
        self.request.session['carrinho'] = carrinho
        self.request.session.save()
        variacao = Variacao.objects.filter(variacao_pk=variacao_id)
        variacao_nome = variacao.produto.nome
        variacao_nome += f'- {variacao.nome}' if variacao_nome else ''
        messages.success(
            self.request,
            f'Produto {variacao_nome} removido do seu carrinho.'
        )

        return redirect(http_referer)


class Carrinho(ListView):
    def get(self, *args, **kwargs):
        carrinho = self.request.session.get('carrinho', {})
        itens = formata_carrinho(carrinho)

        return render(
            self.request,
            'produto/carrinho.html',
            {
                'page_title': 'Carrinho - ',
                'carrinho': itens
            }
        )


class ResumoDaCompra(View):
    def get(self, *args, **kwargs):
        usuario = self.request.user

        if not usuario.is_authenticated:
            return redirect('produto:lista')

        perfil = Perfil.objects.filter(usuario=usuario).first()

        if not self.request.session.get('carrinho'):
            messages.error(
                self.request,
                'Carrinho vazio.'
            )
            return redirect('produto:lista')

        if not perfil:
            return redirect('perfil:criar')

        carrinho = self.request.session.get('carrinho', {})
        itens = formata_carrinho(carrinho)

        return render(
            self.request,
            'produto/resumodacompra.html',
            {
                'page_title': 'Resumo da Compra - ',
                'carrinho': itens
            }
        )
