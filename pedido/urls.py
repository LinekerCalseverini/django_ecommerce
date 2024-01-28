from django.urls import path
from .views import Pagar, SalvarPedido, Detalhe

app_name = 'pedido'

urlpatterns = [
    path('', Pagar.as_view(), name='pagar'),
    path('salvarpedido/', SalvarPedido.as_view(), name='salvarpedido'),
    path('detalhe/<int:pk>', Detalhe.as_view(), name='detalhe'),
]
