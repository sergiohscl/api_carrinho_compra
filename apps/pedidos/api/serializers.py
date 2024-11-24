from rest_framework import serializers
from apps.pedidos.models import InformacaoEnvio


class InformacaoEnvioSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    num_envio = serializers.IntegerField()
    tipo_envio = serializers.CharField(max_length=50)
    custo_envio = serializers.IntegerField()
    num_regiao_envio = serializers.IntegerField(read_only=True)


class DetalhesDoPedidoSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    pedido = serializers.PrimaryKeyRelatedField(read_only=True)
    num_produto = serializers.IntegerField()
    nome_produto = serializers.CharField(max_length=100)
    quantidade = serializers.IntegerField()
    custo_unidade = serializers.FloatField()
    subtotal = serializers.FloatField()


class PedidoSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    num_pedido = serializers.IntegerField()
    data_criacao = serializers.DateTimeField(read_only=True)
    data_envio = serializers.DateTimeField(allow_null=True, required=False)
    info_envio = serializers.PrimaryKeyRelatedField(
        queryset=InformacaoEnvio.objects.all()
    )
    detalhes = DetalhesDoPedidoSerializer(many=True, required=False)
