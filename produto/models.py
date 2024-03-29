# pylint: disable=missing-module-docstring
from PIL import Image
from django.db import models
from django.conf import settings
from utils.rands import slugify_new
from utils.utils import formata_preco

# Create your models here.


class Produto(models.Model):
    '''
    Model para Produtos
    '''
    nome = models.CharField(max_length=255)
    descricao_curta = models.TextField(max_length=255)
    descricao_longa = models.TextField()
    imagem = models.ImageField(
        upload_to='produto_imagens/%Y/%m/', blank=True, null=True
    )
    slug = models.SlugField(unique=True, blank=True, null=True)
    preco_marketing = models.FloatField(verbose_name='Preço')
    preco_marketing_promocional = models.FloatField(
        verbose_name='Preço Promocional',
        default=0.0
    )
    tipo = models.CharField(
        default='V',
        max_length=1,
        choices=(
            ('V', 'Variável'),
            ('S', 'Simples')
        )
    )

    def get_preco_formatado(self):
        '''
        Formatação para mostrar o preço corretamente no Admin.
        '''
        return formata_preco(self.preco_marketing)
    get_preco_formatado.short_description = 'Preço'  # type: ignore

    def get_preco_promocional_formatado(self):
        '''
        Formatação para mostrar o preço promocional corretamente no Admin.
        '''
        return formata_preco(self.preco_marketing_promocional)

    get_preco_promocional_formatado.short_description = (  # type: ignore
        'Preço Promocional'
    )

    def get_descricao_encurtada(self):
        '''
        Formatação para encurtar a descrição em caso dela ser grande demais.
        '''
        if len(self.descricao_curta) < 30:
            return self.descricao_curta

        return self.descricao_curta[:30] + '...'  # pylint: disable=E1136
    get_descricao_encurtada.short_description = 'Descrição'  # type: ignore

    @staticmethod
    def resize_image(img, new_width=800):
        '''
        Vai garantir que a imagem sempre vai ter um tamanho máximo padrão.
        '''
        img_full_path = settings.MEDIA_ROOT / img.name
        img_pil = Image.open(img_full_path)
        original_width, original_height = img_pil.size

        if original_width <= new_width:
            img_pil.close()
            return

        new_height = round((new_width * original_height) / original_width)
        new_img = img_pil.resize(
            (new_width, new_height), Image.LANCZOS  # pylint: disable=no-member
        )
        new_img.save(
            img_full_path,
            optimize=True,
            quality=50
        )

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify_new(self.nome)

        super().save(*args, **kwargs)

        max_image_size = 800
        if self.imagem:
            self.resize_image(self.imagem, max_image_size)

    def __str__(self):
        return str(self.nome)


class Variacao(models.Model):
    '''
    Cada produto pode ter variações (exemplo: uma camiseta pode ter tamanhos
    PP, P, M, G, GG, etc)
    '''
    class Meta:  # pylint: disable=R0903,C0115
        verbose_name = 'Variação'
        verbose_name_plural = 'Variações'

    produto = models.ForeignKey(Produto, on_delete=models.CASCADE)
    nome = models.CharField(max_length=50, blank=True, null=True)
    preco = models.FloatField()
    preco_promocional = models.FloatField(default=0.0)
    estoque = models.PositiveIntegerField(default=1)

    def __str__(self) -> str:
        if not self.nome:
            return self.produto.nome

        return f'{self.produto.nome} - {self.nome}'  # pylint: disable=E1101
