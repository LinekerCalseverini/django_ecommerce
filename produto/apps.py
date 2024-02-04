'''
Módulo para configuração do app produto.
'''
from django.apps import AppConfig


class ProdutoConfig(AppConfig):
    '''
    Configuração do app
    '''
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'produto'
