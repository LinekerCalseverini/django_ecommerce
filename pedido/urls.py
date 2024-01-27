from django.urls import path
from .views import Pagar, FecharPedido, Detalhe

app_name = 'pedido'

urlpatterns = [
    path('', Pagar.as_view(), name='pagar'),
    path('fecharpedido/', FecharPedido.as_view(), name='fecharpedido'),
    path('detalhe/<int:pk>', Detalhe.as_view(), name='detalhe'),
]
