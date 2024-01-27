# pylint: disable=C0114
from django.contrib import admin
from .models import Pedido, ItemPedido


class ItemPedidoInline(admin.TabularInline):
    '''
    Para listar e cadastrar itens de pedido dentro da class Pedido.
    '''
    model = ItemPedido
    extra = 1


class PedidoAdmin(admin.ModelAdmin):
    '''
    Configurando o administrativo do Model Pedido
    '''
    inlines = [
        ItemPedidoInline
    ]


# Register your models here.
admin.site.register(Pedido, PedidoAdmin)
admin.site.register(ItemPedido)
