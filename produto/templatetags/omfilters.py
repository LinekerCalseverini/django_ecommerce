from django.template import Library
from utils.utils import formata_preco, total_carrinho, qtd_carrinho

register = Library()
register.filter(formata_preco)
register.filter(total_carrinho)
register.filter(qtd_carrinho)