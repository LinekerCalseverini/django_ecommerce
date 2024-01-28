from typing import Any
from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views import View
from django.http import HttpResponse
from django.contrib import messages
from .models import Produto, Variacao

# Create your views here.


class ListaProduto(ListView):
    model = Produto
    template_name = 'produto/lista.html'
    context_object_name = 'produtos'
    paginate_by = 12

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

        dados_variacao = carrinho.get(variacao_id, {'quantidade': 0})
        quantidade = dados_variacao.get('quantidade')
        quantidade += 1
        if variacao.estoque < quantidade:
            messages.error(
                self.request,
                'Estoque insuficiente.'
            )
            return redirect(http_referer)
        dados_variacao.update({
            'quantidade': quantidade,
            'preco': variacao.preco,
            'total': quantidade * variacao.preco,
            'imagem': variacao.produto.imagem.url,
            'nome': variacao.produto.nome,
            'variacao': variacao.nome,
            'slug': variacao.produto.slug
        })

        if variacao.preco_promocional:
            dados_variacao['preco'] = variacao.preco_promocional
            dados_variacao['total'] = quantidade * variacao.preco_promocional

        carrinho[variacao_id] = dados_variacao
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
        variacao_data = carrinho.get(variacao_id)

        if not variacao_data:
            return redirect(http_referer)

        carrinho.pop(variacao_id, None)
        self.request.session['carrinho'] = carrinho
        self.request.session.save()
        messages.success(
            self.request,
            f'Produto {variacao_data.get("nome")} removido do seu carrinho.'
        )

        return redirect(http_referer)


class Carrinho(View):
    def get(self, *args, **kwargs):
        return render(self.request, 'produto/carrinho.html',
                      {'page_title': 'Carrinho - '})


class Finalizar(View):
    def get(self, *args, **kwargs):
        return HttpResponse('Finalizar')
