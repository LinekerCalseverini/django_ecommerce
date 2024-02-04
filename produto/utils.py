'''
Módulo de funções utilitárias para o app produto.
'''
from .models import Variacao


def formata_carrinho(carrinho):
    '''
    Função para pegar um carrinho que é composto apenas por VIDs (IDs de Model
    Variacao) em dado bruto para o usuário.
    '''
    vids = list(carrinho)
    variacoes = Variacao.objects.filter(id__in=vids)  # pylint: disable=E1101

    itens = {}
    for variacao in variacoes:
        vid = str(variacao.pk)
        qtd_carrinho = carrinho.get(vid)
        preco = (variacao.preco_promocional
                 if variacao.preco_promocional
                 else variacao.preco)
        itens[vid] = {
            'quantidade': qtd_carrinho,
            'preco': preco,
            'total': preco * qtd_carrinho,
            'imagem': variacao.produto.imagem.url,
            'nome': variacao.produto.nome,
            'variacao': variacao.nome,
            'slug': variacao.produto.slug,
            'variacao_obj': variacao
        }

    return itens
