'''
Módulo para configuração das rotas no app Perfil
'''
from django.urls import path
from .views import Criar, Login, Logout

app_name = 'perfil'  # pylint: disable=C0103

urlpatterns = [
    path('', Criar.as_view(), name='criar'),
    path('login/', Login.as_view(), name='login'),
    path('logout/', Logout.as_view(), name='logout'),
]
