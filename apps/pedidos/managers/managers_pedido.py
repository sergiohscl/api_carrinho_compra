from django.db import models
from apps.pedidos.models import DetalhesDoPedido


class PedidoManager(models.Manager):
    def criar_pedido(self, num_pedido, cliente, estado, info_envio, detalhes):
        # Criação do pedido
        pedido = self.create(
            num_pedido=num_pedido,
            cliente=cliente, estado=estado,
            info_envio=info_envio
        )

        # Adiciona os detalhes do pedido
        for detalhe in detalhes:
            pedido.detalhesdopedido_set.create(
                num_produto=detalhe['num_produto'],
                nome_produto=detalhe['nome_produto'],
                quantidade=detalhe['quantidade'],
                custo_unidade=detalhe['custo_unidade'],
                subtotal=detalhe['quantidade'] * detalhe['custo_unidade']
            )
        return pedido

    def calcular_subtotal(self, pedido):
        # Recalcular subtotal para cada detalhe associado ao pedido
        detalhes = pedido.detalhesdopedido_set.all()
        for detalhe in detalhes:
            detalhe.subtotal = detalhe.quantidade * detalhe.custo_unidade
            detalhe.save()

        # Retorna os detalhes atualizados
        return detalhes

    def update(self, instance, validated_data):
        detalhes_data = validated_data.pop('detalhes', [])
        instance.num_pedido = validated_data.get(
            'num_pedido', instance.num_pedido
        )
        instance.data_envio = validated_data.get(
            'data_envio', instance.data_envio
        )
        instance.cliente = validated_data.get('cliente', instance.cliente)
        instance.estado = validated_data.get('estado', instance.estado)
        instance.info_envio = validated_data.get(
            'info_envio', instance.info_envio
        )
        instance.save()

        # Atualizar ou criar detalhes
        for detalhe_data in detalhes_data:
            detalhe_instance = DetalhesDoPedido.objects.filter(
                pedido=instance,
                num_produto=detalhe_data['num_produto']
            ).first()
            if detalhe_instance:
                for attr, value in detalhe_data.items():
                    setattr(detalhe_instance, attr, value)
                detalhe_instance.save()
            else:
                DetalhesDoPedido.objects.create(
                    pedido=instance, **detalhe_data
                )

        return instance


class InformacaoEnvioManager(models.Manager):

    @staticmethod
    def get_regiao_por_estado():

        return {
            # Centro-Oeste
            'DF': 1, 'GO': 1, 'MT': 1, 'MS': 1,
            # Nordeste
            'AL': 2, 'BA': 2, 'CE': 2, 'MA': 2, 'PB': 2, 'PE': 2, 'PI': 2, 'RN': 2, 'SE': 2, # noqa E501
            # Norte
            'AC': 3, 'AP': 3, 'AM': 3, 'PA': 3, 'RO': 3, 'RR': 3, 'TO': 3,
            # Sudeste
            'ES': 4, 'MG': 4, 'RJ': 4, 'SP': 4,
            # Sul
            'PR': 5, 'RS': 5, 'SC': 5,
        }

    def get_by_id(self, info_envio_id):
        try:
            return self.get(pk=info_envio_id)
        except self.model.DoesNotExist:
            return None

    def atualizar_informacao_envio(self, info_envio_id, validated_data):
        try:
            info_envio = self.get_by_id(info_envio_id)
            for key, value in validated_data.items():
                setattr(info_envio, key, value)
            info_envio.save()
            return info_envio
        except self.model.DoesNotExist:
            return None

    def deletar_informacao_envio(self, info_envio_id):
        try:
            info_envio = self.get_by_id(info_envio_id)
            info_envio.delete()
            return True
        except self.model.DoesNotExist:
            return False
