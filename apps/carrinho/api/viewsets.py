from rest_framework.views import APIView
from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import PermissionDenied
from django_filters.rest_framework import DjangoFilterBackend
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from rest_framework.response import Response
from rest_framework import status
from apps.carrinho.api.serializers import CarrinhoDeComprasSerializer, ProdutoSerializer # noqa E501
from apps.carrinho.managers.manager_carrinho import CarrinhoManager
from apps.carrinho.managers.manager_produto import ProdutosManager
from apps.carrinho.models import CarrinhoDeCompras, Produto
from apps.pedidos.managers.managers_pedido import InformacaoEnvioManager
from apps.pedidos.models import InformacaoEnvio
from apps.perfil.models import Perfil


class ProdutoAPIView(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = ProdutoSerializer
    http_method_names = ['get', 'post']

    @swagger_auto_schema(
        responses={200: ProdutoSerializer(many=True)},
    )
    def get(self, request):
        produtos = Produto.objects.all()
        serializer = ProdutoSerializer(produtos, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @swagger_auto_schema(
        responses={201: ProdutoSerializer(many=False)},
        request_body=ProdutoSerializer
    )
    def post(self, request):
        # Verifica se o usuário logado é administrador
        if not request.user.is_staff:
            raise PermissionDenied(
                "Apenas administradores podem cadastrar produtos."
            )

        serializer = ProdutoSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        try:
            nome = serializer.validated_data.get('nome')
            descricao = serializer.validated_data.get('descricao')
            preco = serializer.validated_data.get('preco')
            estoque = serializer.validated_data.get('estoque')

            manager = ProdutosManager()
            manager.model = Produto

            # Verifica se o produto já existe
            if manager.filter(nome=nome).exists():
                return Response(
                    {'detail': 'Produto já cadastrado.'},
                    status=status.HTTP_400_BAD_REQUEST
                )

            produto = manager.criar_produto(
                nome=nome,
                descricao=descricao,
                preco=preco,
                estoque=estoque
            )

            response_serializer = ProdutoSerializer(produto)
            return Response(
                response_serializer.data, status=status.HTTP_201_CREATED
            )

        except Exception as e:
            return Response(
                {'detail': str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )


class ProdutoDetailAPIView(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = ProdutoSerializer
    http_method_names = ['get', 'put', 'delete']

    @swagger_auto_schema(
        responses={200: ProdutoSerializer(many=False)},
        manual_parameters=[
            openapi.Parameter(
                'UUID', openapi.IN_PATH,
                description="UUID do produto",
                type=openapi.TYPE_STRING
            )
        ],
    )
    def get(self, request, *args, **kwargs):
        produto_uuid = kwargs.get('UUID')
        if not produto_uuid:
            return Response(
                {'detail': 'UUID do produto não fornecido.'},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            produto = Produto.objects.get(num_produto=produto_uuid)
            serializer = ProdutoSerializer(produto)
            return Response(serializer.data, status=status.HTTP_200_OK)

        except Produto.DoesNotExist:
            return Response(
                {'detail': 'Produto não encontrado.'},
                status=status.HTTP_404_NOT_FOUND
            )
        except Exception as e:
            return Response(
                {'detail': str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )

    @swagger_auto_schema(
        request_body=ProdutoSerializer,
        responses={200: ProdutoSerializer(many=False)},
    )
    def put(self, request, *args, **kwargs):
        # Verifica se o usuário logado é administrador
        if not request.user.is_staff:
            raise PermissionDenied(
                "Apenas administradores podem atualizar produtos."
            )

        produto_uuid = kwargs.get('UUID')
        if not produto_uuid:
            return Response(
                {'detail': 'UUID do produto não fornecido.'},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            manager = ProdutosManager()
            produto = manager.update_produto(
                Produto, produto_uuid, request.data
            )

            serializer = ProdutoSerializer(produto)
            return Response(serializer.data, status=status.HTTP_200_OK)

        except Produto.DoesNotExist:
            return Response(
                {'detail': 'Produto não encontrado.'},
                status=status.HTTP_404_NOT_FOUND
            )
        except ValueError as e:
            return Response(
                {'detail': str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )
        except Exception as e:
            return Response(
                {'detail': str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )

    @swagger_auto_schema(
        responses={204: 'Produto deletado com sucesso.'},
        manual_parameters=[
            openapi.Parameter(
                'UUID', openapi.IN_PATH,
                description="UUID do produto",
                type=openapi.TYPE_STRING
            )
        ],
    )
    def delete(self, request, *args, **kwargs):
        # Verifica se o usuário logado é administrador
        if not request.user.is_staff:
            raise PermissionDenied(
                "Apenas administradores podem deletar produtos."
            )

        produto_uuid = kwargs.get('UUID')
        if not produto_uuid:
            return Response(
                {'detail': 'UUID do produto não fornecido.'},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            manager = ProdutosManager()
            manager.delete_produto(Produto, produto_uuid)
            return Response(
                {'detail': 'Produto deletado com sucesso.'},
                status=status.HTTP_204_NO_CONTENT
            )

        except Produto.DoesNotExist:
            return Response(
                {'detail': 'Produto não encontrado.'},
                status=status.HTTP_404_NOT_FOUND
            )
        except Exception as e:
            return Response(
                {'detail': str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )


class ProdutoFilterListAPIView(ListAPIView):
    queryset = Produto.objects.all()
    serializer_class = ProdutoSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['num_produto', 'nome']

    @swagger_auto_schema(
        responses={200: ProdutoSerializer(many=True)},
        manual_parameters=[
            openapi.Parameter(
                'num_produto', openapi.IN_QUERY,
                description="UUID do produto (parcial ou completo)",
                type=openapi.TYPE_STRING
            ),
            openapi.Parameter(
                'nome', openapi.IN_QUERY,
                description="Nome do produto (parcial ou completo)",
                type=openapi.TYPE_STRING
            )
        ],
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)


class CarrinhoAPIView(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = CarrinhoDeComprasSerializer
    http_method_names = ['get', 'post']

    @swagger_auto_schema(
        responses={200: CarrinhoDeComprasSerializer(many=True)},
    )
    def get(self, request):
        try:
            cliente = Perfil.objects.get(usuario=request.user)

            # Usando o CarrinhoManager para buscar carrinhos
            carrinhos = CarrinhoDeCompras.objects.filter(
                cliente=cliente, status='A'
            )

            if not carrinhos.exists():
                return Response(
                    {"detail": "Nenhum carrinho ativo encontrado."},
                    status=status.HTTP_404_NOT_FOUND
                )

            serializer = self.serializer_class(carrinhos, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)

        except Perfil.DoesNotExist:
            return Response(
                {"detail": "Perfil do cliente não encontrado."},
                status=status.HTTP_404_NOT_FOUND
            )

    @swagger_auto_schema(
        responses={201: CarrinhoDeComprasSerializer(many=False)},
        request_body=CarrinhoDeComprasSerializer
    )
    def post(self, request):

        try:
            # Instancia o manager manualmente
            carrinho_manager = CarrinhoManager()

            # Utiliza o manager para criar o carrinho vazio
            carrinho = carrinho_manager.criar_carrinho_vazio(
                cliente=request.user.perfil
            )

            # Serializa o carrinho criado
            response_serializer = CarrinhoDeComprasSerializer(carrinho)
            return Response(
                response_serializer.data, status=status.HTTP_201_CREATED
            )

        except Exception as e:
            return Response(
                {'detail': str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )


class CarrinhoComprasAPIView(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = CarrinhoDeComprasSerializer
    http_method_names = ['post',]

    @swagger_auto_schema(
        responses={201: CarrinhoDeComprasSerializer(many=False)}
    )
    def post(self, request, num_produto, quantidade):
        try:
            carrinho_manager = CarrinhoManager()

            # Obtém o carrinho ativo
            carrinho = carrinho_manager.get_carrinho_ativo(request.user.perfil)
            if not carrinho:
                return Response(
                    {"detail": "Carrinho ativo não encontrado."},
                    status=status.HTTP_404_NOT_FOUND
                )

            # Verifica se o produto existe
            try:
                produto = Produto.objects.get(num_produto=num_produto)
            except Produto.DoesNotExist:
                return Response(
                    {"detail": "Produto não encontrado."},
                    status=status.HTTP_404_NOT_FOUND
                )

            # Adiciona o produto ao carrinho
            try:
                carrinho = carrinho_manager.add_produto_carrinho(
                    carrinho, produto, quantidade
                )
            except ValueError as e:
                return Response(
                    {"detail": str(e)},
                    status=status.HTTP_400_BAD_REQUEST
                )

            # Determina o frete automaticamente com base na região do cliente
            try:
                perfil = request.user.perfil
                endereco = perfil.enderecos.first()
                if not endereco or not endereco.estado:
                    return Response(
                        {"detail": "Endereço ou estado do cliente não encontrado."}, # noqa E501
                        status=status.HTTP_400_BAD_REQUEST
                    )

                # Obter o número da região com base no estado
                manager = InformacaoEnvioManager()
                regiao_por_estado = manager.get_regiao_por_estado()
                estado_cliente = endereco.estado.upper()

                num_regiao_envio = regiao_por_estado.get(estado_cliente)
                if not num_regiao_envio:
                    return Response(
                        {"detail": f"Estado '{estado_cliente}' não mapeado para nenhuma região."}, # noqa E501
                        status=status.HTTP_400_BAD_REQUEST
                    )

                # Obter a informação de envio com base na região
                frete = InformacaoEnvio.objects.filter(
                    num_regiao_envio=num_regiao_envio
                ).first()
                if not frete:
                    return Response(
                        {"detail": f"Não há informações de envio disponíveis para a região {num_regiao_envio}."}, # noqa E501
                        status=status.HTTP_400_BAD_REQUEST
                    )

                # Atribuir o frete ao carrinho
                carrinho_manager.atribuir_frete(carrinho, frete.id)

            except Exception as e:
                return Response(
                    {"detail": f"Erro ao determinar frete: {str(e)}"},
                    status=status.HTTP_400_BAD_REQUEST
                )

            # Calcula o total com o frete
            total_com_frete = carrinho_manager.calcular_total_com_frete(
                carrinho
            )

            return Response(
                {
                    "detail": "Produto adicionado ao carrinho com sucesso.",
                    "carrinho": {
                        "id": carrinho.id,
                        "itens": carrinho.itens,
                        "frete": carrinho.frete.custo_envio if carrinho.frete else 0.0, # noqa E501
                        "total": total_com_frete,
                    }
                },
                status=status.HTTP_200_OK,
            )

        except Exception as e:
            return Response(
                {"detail": str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )


class RemoveCarrinhoComprasAPIView(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = CarrinhoDeComprasSerializer
    http_method_names = ['delete',]

    @swagger_auto_schema(
        responses={200: "Item removido e atualizado no carrinho com sucesso."},
        operation_description="Remove um item do carrinho, decrementa sua quantidade e atualiza o estoque do produto." # noqa E501
    )
    def delete(self, request, nome=None, quantidade=1):
        try:
            carrinho_manager = CarrinhoManager()

            # Obtém o carrinho ativo
            carrinho = carrinho_manager.get_carrinho_ativo(request.user.perfil)
            if not carrinho:
                return Response(
                    {"detail": "Carrinho ativo não encontrado."},
                    status=status.HTTP_404_NOT_FOUND
                )

            # Verifica se o produto existe no carrinho pelo nome
            itens = carrinho.itens
            produto_key = None

            for key, item in itens.items():
                if item.get('nome') == nome:
                    produto_key = key
                    break

            if not produto_key:
                return Response(
                    {"detail": f"Produto '{nome}' não encontrado no carrinho."}, # noqa E501
                    status=status.HTTP_404_NOT_FOUND
                )

            # Restaura o estoque do produto
            try:
                produto = Produto.objects.get(id=produto_key)
            except Produto.DoesNotExist:
                return Response(
                    {"detail": "Produto não encontrado no banco de dados."},
                    status=status.HTTP_404_NOT_FOUND
                )

            # Decrementa a quantidade no carrinho
            quantidade_removida = min(
                quantidade, itens[produto_key]['quantidade']
            )
            produto.estoque += quantidade_removida
            produto.save()

            itens[produto_key]['quantidade'] -= quantidade_removida
            itens[produto_key]['subtotal'] = itens[produto_key]['quantidade'] * produto.preco # noqa E501

            # Remove o item se a quantidade for zero
            if itens[produto_key]['quantidade'] <= 0:
                del itens[produto_key]

            # Atualiza o carrinho
            carrinho.itens = itens
            carrinho.total = sum(item['subtotal'] for item in itens.values())
            carrinho.save()

            return Response(
                {"detail": f"Item '{nome}' removido ou atualizado no carrinho com sucesso."}, # noqa E501
                status=status.HTTP_200_OK
            )

        except Exception as e:
            return Response(
                {"detail": str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )


class AtualizarStatusCarrinhoAPIView(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = CarrinhoDeComprasSerializer
    http_method_names = ['patch']

    @swagger_auto_schema(
        request_body=CarrinhoDeComprasSerializer,
        responses={200: "Status do carrinho atualizado com sucesso."},
        operation_description="Atualiza o status do carrinho."
    )
    def patch(self, request):
        try:
            # Obtém o carrinho ativo
            carrinho_manager = CarrinhoManager()
            carrinho = carrinho_manager.get_carrinho_ativo(request.user.perfil)

            if not carrinho:
                return Response(
                    {"detail": "Carrinho ativo não encontrado."},
                    status=status.HTTP_404_NOT_FOUND
                )

            # Obtém o novo status enviado no corpo da requisição
            novo_status = request.data.get('status')
            if not novo_status:
                return Response(
                    {"detail": "É necessário fornecer o novo status."},
                    status=status.HTTP_400_BAD_REQUEST
                )

            # Atualiza o status do carrinho
            carrinho.status = novo_status
            carrinho.save()

            return Response(
                {
                    "detail": "Status do carrinho atualizado com sucesso.",
                    "carrinho": {
                        "id": carrinho.id,
                        "status": carrinho.status
                    }
                },
                status=status.HTTP_200_OK
            )

        except Exception as e:
            return Response(
                {"detail": str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )


class ListarCarrinhosFinalizadosAPIView(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = CarrinhoDeComprasSerializer
    http_method_names = ['get']

    @swagger_auto_schema(
        responses={200: CarrinhoDeComprasSerializer(many=True)},
        operation_description="Lista todos os carrinhos com status 'Finalizado'." # noqa E501
    )
    def get(self, request):
        try:
            carrinhos = CarrinhoDeCompras.objects.filter(
                cliente=request.user.perfil,
                status=CarrinhoDeCompras.StatusCarrinho.FINALIZADO
            )

            # Valida se há carrinhos finalizados
            if not carrinhos.exists():
                return Response(
                    {"detail": "Nenhum carrinho finalizado encontrado."},
                    status=status.HTTP_404_NOT_FOUND
                )

            # Serializa os carrinhos encontrados
            serializer = self.serializer_class(carrinhos, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)

        except Exception as e:
            return Response(
                {"detail": str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )
