from django.template import Library
from utils.utils import formata_preco

register = Library()
register.filter(formata_preco)
