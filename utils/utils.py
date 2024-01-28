def formata_preco(val):
    return (f'R$ {val:,.2f}'.replace(',', '^')
            .replace('.', ',').replace('^', '.'))


def total_carrinho(carrinho):
    total = sum([item['total'] for item in carrinho.values()])

    return total


def qtd_carrinho(carrinho):
    total = sum([item['quantidade'] for item in carrinho.values()])

    return total
