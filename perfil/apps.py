'''
Módulo para definição de Configuração do Perfil
'''
from django.apps import AppConfig


class PerfilConfig(AppConfig):
    '''
    Configuração do app
    '''
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'perfil'
