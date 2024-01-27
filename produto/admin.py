# pylint: disable=missing-module-docstring
from django.contrib import admin
from .models import Produto, Variacao


class VariacaoInline(admin.TabularInline):
    '''
    Inline para a variação aparecer dentro do Produto
    '''
    model = Variacao
    extra = 1


class ProdutoAdmin(admin.ModelAdmin):
    '''
    Classe para administração de Model Produto
    '''
    list_display = ['nome', 'get_descricao_encurtada',
                    'get_preco_formatado', 'get_preco_promocional_formatado']
    inlines = [
        VariacaoInline
    ]


# Register your models here.
admin.site.register(Produto, ProdutoAdmin)
admin.site.register(Variacao)
