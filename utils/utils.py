'''
Funções utilitárias para o app geral.
'''


def formata_preco(val):
    '''
    Usado em filtros do django para formatar o preço no padrão de moeda.
    '''
    return (f'R$ {val:,.2f}'.replace(',', '^')
            .replace('.', ',').replace('^', '.'))


def total_carrinho(carrinho):
    '''
    Usado em filtros para identificar qual o preço total atual no carrinho. Só
    aceita carrinhos formatados.
    '''
    total = sum([item['total'] for item in carrinho.values()])

    return total


def qtd_carrinho(carrinho):
    '''
    Usado em filtros para identificar quantos itens há no carrinho. Só aceita
    carrinhos que ainda não foram formatados.
    '''
    total = sum(list(carrinho.values()))

    return total


def multiply(value, multiplier):
    '''
    Usado em filtros para multiplicar valores.
    '''
    return value * multiplier
