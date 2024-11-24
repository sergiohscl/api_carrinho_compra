from django.db import models
from apps.perfil.models import Perfil


class InformacaoEnvio(models.Model):
    REGIAO_CHOICES = [
        (1, 'Centro-Oeste'),
        (2, 'Nordeste'),
        (3, 'Norte'),
        (4, 'Sudeste'),
        (5, 'Sul'),
    ]

    num_envio = models.IntegerField(unique=True)
    tipo_envio = models.CharField(max_length=50)
    custo_envio = models.IntegerField()
    num_regiao_envio = models.IntegerField(
        choices=REGIAO_CHOICES,
        null=True,
        blank=True,
        default=None
    )

    class Meta:
        verbose_name = 'Informação de Envio'
        verbose_name_plural = 'Informações de Envio'

    def __str__(self):
        return f"Envio {self.num_envio} - Tipo: {self.tipo_envio}"


class Pedido(models.Model):
    num_pedido = models.IntegerField(unique=True)
    data_criacao = models.DateTimeField(auto_now_add=True)
    data_envio = models.DateTimeField(null=True, blank=True)
    cliente = models.ForeignKey(Perfil, on_delete=models.CASCADE)
    estado = models.CharField(max_length=50)
    info_envio = models.ForeignKey(InformacaoEnvio, on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'Pedido'
        verbose_name_plural = 'Pedidos'

    def __str__(self):
        return f"Pedido {self.num_pedido} do cliente {self.cliente}"


class DetalhesDoPedido(models.Model):
    pedido = models.ForeignKey(Pedido, on_delete=models.CASCADE)
    num_produto = models.IntegerField()
    nome_produto = models.CharField(max_length=100)
    quantidade = models.IntegerField()
    custo_unidade = models.FloatField()
    subtotal = models.FloatField()

    class Meta:
        verbose_name = 'Detalhe do Pedido'
        verbose_name_plural = 'Detalhes do Pedido'

    def __str__(self):
        return f"Detalhe do pedido {self.pedido.num_pedido} - Produto: {self.nome_produto}" # noqa E501
