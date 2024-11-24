from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from apps.pedidos.managers.managers_pedido import InformacaoEnvioManager, PedidoManager  # noqa E501
from apps.pedidos.models import DetalhesDoPedido, Pedido, InformacaoEnvio
from apps.perfil.models import Perfil
from .serializers import DetalhesDoPedidoSerializer, PedidoSerializer, InformacaoEnvioSerializer # noqa E501
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from rest_framework.parsers import JSONParser
from rest_framework.exceptions import NotFound


class InformacaoEnvioAPIView(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = InformacaoEnvioSerializer
    http_method_names = ['get', 'post']

    @swagger_auto_schema(
        responses={200: InformacaoEnvioSerializer(many=True)},
    )
    def get(self, request, *args, **kwargs):
        infos = InformacaoEnvio.objects.all()
        serializer = InformacaoEnvioSerializer(infos, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @swagger_auto_schema(
        responses={201: InformacaoEnvioSerializer(many=False)},
        request_body=InformacaoEnvioSerializer
    )
    def post(self, request, *args, **kwargs):
        serializer = InformacaoEnvioSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        try:
            # Obter o mapeamento de regiões
            manager = InformacaoEnvioManager()
            manager.model = InformacaoEnvio
            regiao_por_estado = manager.get_regiao_por_estado()

            # Verificar se o perfil e o endereço existem
            perfil = getattr(request.user, 'perfil', None)
            if not perfil:
                return Response(
                    {'detail': 'Perfil do usuário não encontrado.'},
                    status=status.HTTP_400_BAD_REQUEST
                )

            endereco = perfil.enderecos.first()
            if not endereco or not endereco.estado:
                return Response(
                    {'detail': 'Endereço ou estado do usuário não encontrado.'}, # noqa E501
                    status=status.HTTP_400_BAD_REQUEST
                )

            # Obter o número da região com base no estado
            estado = endereco.estado
            num_regiao_envio = regiao_por_estado.get(estado)

            if num_regiao_envio is None:
                return Response(
                    {'detail': f"Estado {estado} não mapeado para nenhuma região."}, # noqa E501
                    status=status.HTTP_400_BAD_REQUEST
                )

            # Criar a informação de envio com a região associada
            info_envio = InformacaoEnvio.objects.create(
                num_envio=serializer.validated_data['num_envio'],
                tipo_envio=serializer.validated_data['tipo_envio'],
                custo_envio=serializer.validated_data['custo_envio'],
                num_regiao_envio=num_regiao_envio
            )

            response_serializer = InformacaoEnvioSerializer(info_envio)
            return Response(
                response_serializer.data, status=status.HTTP_201_CREATED
            )

        except Exception as e:
            return Response(
                {'detail': str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class InformacaoEnvioDetails(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = InformacaoEnvioSerializer
    http_method_names = ['get', 'put', 'delete']

    @swagger_auto_schema(
        responses={200: InformacaoEnvioSerializer(many=False)},
        manual_parameters=[
            openapi.Parameter(
                'id', openapi.IN_PATH,
                description="ID da informação de envio",
                type=openapi.TYPE_INTEGER
            )
        ],
    )
    def get(self, request, *args, **kwargs):
        info_envio_id = kwargs.get('pk')
        if not info_envio_id:
            return Response(
                {'detail': 'ID do info_envio não fornecido.'},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            manager = InformacaoEnvioManager()
            manager.model = InformacaoEnvio
            info_envio = manager.get_by_id(info_envio_id)

            if not info_envio:
                return Response(
                    {'detail': 'Informação de envio não encontrado.'},
                    status=status.HTTP_404_NOT_FOUND
                )
            serializer = InformacaoEnvioSerializer(info_envio)
            return Response(serializer.data, status=status.HTTP_200_OK)

        except Exception as e:
            return Response(
                {'detail': str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )

    @swagger_auto_schema(
        responses={200: InformacaoEnvioSerializer(many=False)},
        request_body=InformacaoEnvioSerializer,
        manual_parameters=[
            openapi.Parameter(
                'id', openapi.IN_PATH,
                description="ID da informação de envio",
                type=openapi.TYPE_INTEGER
            )
        ],
    )
    def put(self, request, *args, **kwargs):
        info_envio_id = kwargs.get('pk')
        if not info_envio_id:
            return Response(
                {'detail': 'ID da informação de envio não fornecido.'},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            serializer = InformacaoEnvioSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)

            manager = InformacaoEnvioManager()
            manager.model = InformacaoEnvio
            info_envio = manager.atualizar_informacao_envio(
                info_envio_id, serializer.validated_data
            )

            if not info_envio:
                return Response(
                    {'detail': 'Informação de envio não encontrada.'},
                    status=status.HTTP_404_NOT_FOUND
                )

            response_serializer = InformacaoEnvioSerializer(info_envio)
            return Response(
                response_serializer.data, status=status.HTTP_200_OK
            )
        except InformacaoEnvio.DoesNotExist:
            return Response(
                {'detail': 'Informação de envio não encontrada.'},
                status=status.HTTP_404_NOT_FOUND
            )
        except Exception as e:
            return Response(
                {'detail': f'Erro ao atualizar informação de envio: {str(e)}'},
                status=status.HTTP_400_BAD_REQUEST
            )

    @swagger_auto_schema(
        responses={204: 'Informação de envio deletada com sucesso.'},
        manual_parameters=[
            openapi.Parameter(
                'id', openapi.IN_PATH,
                description="ID da informação de envio",
                type=openapi.TYPE_INTEGER
            )
        ],
    )
    def delete(self, request, *args, **kwargs):
        info_envio_id = kwargs.get('pk')
        if not info_envio_id:
            return Response(
                {'detail': 'ID da informação de envio não fornecido.'},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            manager = InformacaoEnvioManager()
            manager.model = InformacaoEnvio
            sucesso = manager.deletar_informacao_envio(info_envio_id)

            if not sucesso:
                return Response(
                    {'detail': 'Informação de envio não encontrada.'},
                    status=status.HTTP_404_NOT_FOUND
                )

            return Response(
                {'detail': 'Informação de envio deletada com sucesso.'},
                status=status.HTTP_204_NO_CONTENT
            )
        except Exception as e:
            return Response(
                {'detail': f'Erro ao deletar informação de envio: {str(e)}'},
                status=status.HTTP_400_BAD_REQUEST
            )


class PedidoAPIView(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = PedidoSerializer
    http_method_names = ['get', 'post']
    parser_classes = [JSONParser]

    @swagger_auto_schema(
        responses={200: PedidoSerializer(many=True)}
    )
    def get(self, request, *args, **kwargs):
        try:
            # Instanciar o manager diretamente
            pedido_manager = PedidoManager()
            pedido_manager.model = Pedido  # Associar o modelo ao manager

            # Obter pedidos
            pedidos = pedido_manager.all()

            # Montar os dados manualmente para incluir os detalhes
            pedidos_com_detalhes = []
            for pedido in pedidos:
                detalhes = DetalhesDoPedido.objects.filter(pedido=pedido)
                detalhes_serializados = DetalhesDoPedidoSerializer(
                    detalhes, many=True
                ).data

                pedido_data = PedidoSerializer(pedido).data
                pedido_data['detalhes'] = detalhes_serializados
                pedidos_com_detalhes.append(pedido_data)

            return Response(pedidos_com_detalhes, status=status.HTTP_200_OK)
        except Exception as e:
            return Response(
                {'detail': f'Erro ao listar pedidos: {str(e)}'},
                status=status.HTTP_400_BAD_REQUEST
            )

    @swagger_auto_schema(
        responses={201: PedidoSerializer(many=False)},
        request_body=PedidoSerializer
    )
    def post(self, request, *args, **kwargs):
        serializer = PedidoSerializer(data=request.data)
        if serializer.is_valid():
            try:

                try:
                    cliente = request.user.perfil
                except Perfil.DoesNotExist:
                    raise NotFound("Perfil do usuário logado não encontrado.")

                # Determinar o estado a partir do perfil do cliente
                if cliente.enderecos.exists():
                    estado = cliente.enderecos.first().estado
                else:
                    raise NotFound(
                        "Endereço associado ao cliente não encontrado."
                    )

                # Extraindo os dados validados
                detalhes_data = serializer.validated_data.pop('detalhes', [])
                num_pedido = serializer.validated_data.get('num_pedido')
                info_envio = serializer.validated_data.get('info_envio')
                data_envio = serializer.validated_data.get('data_envio')

                if data_envio is None:
                    from django.utils.timezone import now
                    data_envio = now()

                # Criando o pedido
                pedido_manager = PedidoManager()
                pedido_manager.model = Pedido
                pedido = pedido_manager.create(
                    num_pedido=num_pedido,
                    cliente=cliente,
                    estado=estado,
                    info_envio=info_envio,
                    data_envio=data_envio
                )

                # Criar os detalhes do pedido
                for detalhe in detalhes_data:
                    DetalhesDoPedido.objects.create(
                        pedido=pedido,
                        **detalhe
                    )

                # Recalcular os subtotais dos detalhes do pedido
                pedido_manager.calcular_subtotal(pedido)

                # Serializar o pedido e adicionar os detalhes atualizados
                detalhes_serializados = DetalhesDoPedidoSerializer(
                    pedido.detalhesdopedido_set.all(), many=True
                ).data

                # Retornar os dados completos do pedido
                pedido_data = {
                    "id": pedido.id,
                    "num_pedido": pedido.num_pedido,
                    "data_criacao": pedido.data_criacao,
                    "data_envio": pedido.data_envio,
                    "info_envio": pedido.info_envio.id,
                    "cliente": {
                        "id": cliente.usuario.id,
                        "username": cliente.usuario.username,
                        "email": cliente.usuario.email
                    },
                    "estado": estado,
                    "detalhes": detalhes_serializados,
                }

                return Response(pedido_data, status=status.HTTP_201_CREATED)
            except Exception as e:
                return Response(
                    {'detail': f'Erro ao criar pedido: {str(e)}'},
                    status=status.HTTP_400_BAD_REQUEST
                )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PedidoDetailsAPIView(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = PedidoSerializer
    http_method_names = ['delete',]
    parser_classes = [JSONParser]

    @swagger_auto_schema(
        responses={204: 'Pedido deletado com sucesso.'},
        manual_parameters=[
            openapi.Parameter(
                'id', openapi.IN_PATH,
                description="ID do pedido a ser deletado",
                type=openapi.TYPE_INTEGER,
                required=True
            )
        ]
    )
    def delete(self, request, *args, **kwargs):
        try:
            # Recuperar o ID do pedido a partir da URL
            pedido_id = kwargs.get('id')
            if not pedido_id:
                return Response(
                    {'detail': 'ID do pedido não fornecido.'},
                    status=status.HTTP_400_BAD_REQUEST
                )

            # Tentar buscar o pedido
            pedido = Pedido.objects.filter(id=pedido_id).first()
            if not pedido:
                return Response(
                    {'detail': 'Pedido não encontrado.'},
                    status=status.HTTP_404_NOT_FOUND
                )

            # Deletar o pedido e os detalhes associados
            pedido.delete()

            return Response(
                {'detail': 'Pedido deletado com sucesso.'},
                status=status.HTTP_204_NO_CONTENT
            )
        except Exception as e:
            return Response(
                {'detail': f'Erro ao deletar pedido: {str(e)}'},
                status=status.HTTP_400_BAD_REQUEST
            )
