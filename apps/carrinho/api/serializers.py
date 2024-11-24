from rest_framework import serializers
from apps.carrinho.models import CarrinhoDeCompras
# from apps.pedidos.models import InformacaoEnvio


class ProdutoSerializer(serializers.Serializer):
    num_produto = serializers.UUIDField(read_only=True)
    nome = serializers.CharField(max_length=100)
    descricao = serializers.CharField(allow_blank=True, required=False)
    preco = serializers.FloatField()
    estoque = serializers.IntegerField()


class CarrinhoDeComprasSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    cliente = serializers.PrimaryKeyRelatedField(read_only=True)
    itens = serializers.JSONField()
    frete_custo = serializers.SerializerMethodField()
    total = serializers.FloatField(required=False, allow_null=True)
    status = serializers.ChoiceField(
        choices=CarrinhoDeCompras.StatusCarrinho.choices
    )

    def get_frete_custo(self, obj):

        if obj.frete:
            return obj.frete.custo_envio
        return None
