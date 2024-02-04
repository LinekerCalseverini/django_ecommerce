'''
Módulo que controla as views do app produto.
'''
# pylint: disable=E1101,W0613
from typing import Any
from django.db.models.query import QuerySet
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views import View
from django.contrib import messages
from django.db.models import Q
from perfil.models import Perfil
from .models import Produto, Variacao
from .utils import formata_carrinho

# Create your views here.


class ListaProduto(ListView):
    '''
    View que controla como a lista de produtos será renderizada.
    '''
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


class Busca(ListaProduto):
    '''
    View que define como renderizar quando existem termos no campo de busca.
    '''

    def get(self, request, *args, **kwargs):
        termo = self.request.GET.get('termo', '').strip()
        if not termo:
            return redirect('produto:lista')

        return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        ctx = super().get_context_data(**kwargs)
        termo = self.request.GET.get("termo", "")
        ctx.update({
            'page_title': f'{termo} - Busca - '
        })
        return ctx

    def get_queryset(self) -> QuerySet[Any]:
        qs = super().get_queryset()
        termo = self.request.GET.get('termo', '').strip()

        if not termo:
            return qs

        return qs.filter(
            Q(nome__icontains=termo) |
            Q(descricao_curta__icontains=termo) |
            Q(descricao_longa__icontains=termo)
        )


class DetalheProduto(DetailView):
    '''
    View que define como a página de detalhes de um produto será renderizada.
    '''
    model = Produto
    template_name = 'produto/detalhe.html'
    context_object_name = 'produto'
    slug_url_kwarg = 'slug'

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        ctx = super().get_context_data(**kwargs)
        produto = self.get_object()

        ctx.update({
            'page_title': f'Comprar {produto.nome} - '  # type: ignore
        })

        return ctx


class AdicionarAoCarrinho(View):
    '''
    View que define a função de adicionar um produto ao Carrinho. Redireciona
    para a página de carrinho.
    '''

    def get(self, *args, **kwargs):
        '''
        Função que define como esta view responderá a requests do tipo GET.
        '''
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
    '''
    View que define como a função de remoção do carrinho vai funcionar.
    '''

    def get(self, *args, **kwargs):
        '''
        View que define como a remoção do carrinho vai responder a requisições
        GET.
        '''
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
        variacao_nome = variacao.produto.nome   # type: ignore
        variacao_nome += (f'- {variacao.nome}'  # type: ignore
                          if variacao_nome else '')
        messages.success(
            self.request,
            f'Produto {variacao_nome} removido do seu carrinho.'
        )

        return redirect(http_referer)


class Carrinho(ListView):
    '''
    View que define como a página de carrinho será renderizada.
    '''

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
    '''
    View que define como a página de resumo da compra (antes da página de
    pagamento) será renderizada.
    '''

    def get(self, *args, **kwargs):
        '''
        Função que define como a view responderá a requisições http GET.
        '''
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
