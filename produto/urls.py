# pylint: disable=C0114
from django.urls import path
from .views import (
    ListaProduto, DetalheProduto, AdicionarAoCarrinho, RemoverDoCarrinho,
    Carrinho, ResumoDaCompra, Busca
)

app_name = 'produto'  # pylint: disable=C0103

urlpatterns = [
    path('', ListaProduto.as_view(), name='lista'),
    path('produto/<slug:slug>/', DetalheProduto.as_view(), name='detalhe'),
    path('adicionaraocarrinho/', AdicionarAoCarrinho.as_view(),
         name='adicionaraocarrinho'),
    path('removerdocarrinho/', RemoverDoCarrinho.as_view(),
         name='removerdocarrinho'),
    path('carrinho/', Carrinho.as_view(), name='carrinho'),
    path('resumodacompra/', ResumoDaCompra.as_view(), name='resumodacompra'),
    path('busca/', Busca.as_view(), name='busca'),
]
