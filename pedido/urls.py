from django.urls import path
from .views import Pagar, SalvarPedido, Detalhe, ListaPedido

app_name = 'pedido'

urlpatterns = [
    path('', Pagar.as_view(), name='pagar'),
    path('salvarpedido/', SalvarPedido.as_view(), name='salvarpedido'),
    path('lista/', ListaPedido.as_view(), name='lista'),
    path('detalhe/<int:pk>', Detalhe.as_view(), name='detalhe'),
]
