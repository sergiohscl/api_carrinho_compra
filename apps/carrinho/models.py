from uuid import uuid4
from django.db import models
from apps.pedidos.models import InformacaoEnvio
from apps.perfil.models import Perfil


class Produto(models.Model):
    num_produto = models.UUIDField(
        default=uuid4,
        editable=False,
        unique=True
    )
    nome = models.CharField(max_length=100)
    descricao = models.TextField(blank=True, null=True)
    preco = models.FloatField()
    estoque = models.IntegerField()

    class Meta:
        verbose_name = 'Produto'
        verbose_name_plural = 'Produtos'

    def __str__(self):
        return f"Produto: {self.nome}"


class CarrinhoDeCompras(models.Model):
    class StatusCarrinho(models.TextChoices):
        ATIVO = 'A', 'Ativo'
        FINALIZADO = 'F', 'Finalizado'

    cliente = models.ForeignKey(
        Perfil,
        on_delete=models.CASCADE,
        related_name="carrinhos"
    )
    itens = models.JSONField(
        default=dict,
        help_text="Estrutura: {'produto_id': {'nome': str, 'descricao': str, 'preco': float, 'quantidade': int}}" # noqa E501
    )
    frete = models.ForeignKey(
        InformacaoEnvio,
        on_delete=models.CASCADE,
        related_name="carrinhos_envio",
        blank=True,
        null=True
    )
    total = models.FloatField(blank=True, null=True)
    status = models.CharField(
        max_length=1,
        choices=StatusCarrinho.choices,
        default=StatusCarrinho.ATIVO
    )

    class Meta:
        verbose_name = 'Carrinho de Compras'
        verbose_name_plural = 'Carrinhos de Compras'

    def __str__(self):
        return f"Carrinho {self.id} do cliente {self.cliente}"
