# pylint: disable=C0114
from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class Pedido(models.Model):
    '''
    Classe que identifica o objeto de Pedido.
    '''
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    total = models.FloatField()
    status = models.CharField(
        default='C',
        max_length=1,
        choices=(
            ('A', 'Aprovado'),
            ('C', 'Criado'),
            ('R', 'Reprovado'),
            ('P', 'Pendente'),
            ('E', 'Enviado'),
            ('F', 'Finalizado'),
        )
    )

    def __str__(self) -> str:
        return f'Pedido N. {self.pk}'


class ItemPedido(models.Model):
    '''
    Classe que define os objetos de itens que pertencem a um pedido em
    específico.
    '''
    class Meta:  # pylint: disable=C0115,R0903
        verbose_name = 'Item do Pedido'
        verbose_name_plural = 'Itens do Pedido'

    pedido = models.ForeignKey(Pedido, on_delete=models.CASCADE)
    produto = models.CharField(max_length=255)
    produto_id = models.PositiveIntegerField()
    variacao = models.CharField(max_length=255)
    variacao_id = models.PositiveIntegerField()
    preco = models.FloatField()
    preco_promocional = models.FloatField(default=0.0)
    quantidade = models.PositiveIntegerField()
    imagem = models.CharField(max_length=2048)

    def __str__(self) -> str:
        return f'Item do {self.pedido}'
