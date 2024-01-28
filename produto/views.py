from typing import Any
from django.db.models.query import QuerySet
from django.shortcuts import redirect, reverse, get_object_or_404
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
        return HttpResponse('RemoverDoCarrinho')


class Carrinho(ListView):
    template_name = 'produto/carrinho.html'
    context_object_name = 'itens'

    def get_queryset(self) -> QuerySet[Any]:
        variacao_ids = self.request.session.get('carrinho', {}).keys()
        query_set = Variacao.objects.filter(id__in=variacao_ids)

        return query_set


class Finalizar(View):
    def get(self, *args, **kwargs):
        return HttpResponse('Finalizar')
