from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import PermissionDenied
from rest_framework.status import HTTP_200_OK, HTTP_201_CREATED, HTTP_400_BAD_REQUEST # noqa E501
from apps.perfil.api.serializers import UsuarioSerializer, PerfilSerializer, EnderecoSerializer # noqa E501
from apps.perfil.managers.managers import UsuarioManager, PerfilManager, EnderecoManager # noqa E501
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from drf_yasg import openapi

from apps.perfil.models import Perfil


class UsuarioAPIView(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = UsuarioSerializer
    http_method_names = ['get', 'post']

    @swagger_auto_schema(
        responses={200: UsuarioSerializer(many=True)},
    )
    def get(self, request):
        usuarios = UsuarioManager.listar_usuarios()
        serializer = UsuarioSerializer(usuarios, many=True)
        return Response(serializer.data, status=HTTP_200_OK)

    @swagger_auto_schema(
        responses={201: UsuarioSerializer(many=False)},
        request_body=UsuarioSerializer
    )
    def post(self, request):
        serializer = UsuarioSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        try:
            username = serializer.validated_data.get('username')
            email = serializer.validated_data.get('email')
            password = serializer.validated_data.get('password')

            manager = UsuarioManager()

            # Verifica se o usuário já existe com o mesmo e-mail
            if manager.get_by_email(email).exists():
                return Response(
                    {'detail': 'Usuário com este email já existe.'},
                    status=status.HTTP_400_BAD_REQUEST
                )

            # Criação do usuário
            usuario = manager.criar_usuario(
                username=username,
                email=email,
                password=password
            )

            # Serializa e retorna a resposta
            response_serializer = UsuarioSerializer(usuario)
            return Response(
                response_serializer.data, status=status.HTTP_201_CREATED
            )

        except Exception as e:
            return Response(
                {'detail': str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )


class UsuarioDetailAPIView(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = UsuarioSerializer
    http_method_names = ['get', 'delete']

    @swagger_auto_schema(
        responses={200: UsuarioSerializer(many=False)},
        manual_parameters=[
            openapi.Parameter(
                'id', openapi.IN_PATH,
                description="ID do usuário",
                type=openapi.TYPE_STRING
            )
        ],
    )
    def get(self, request, *args, **kwargs):
        user_id = kwargs.get('pk')
        if not user_id:
            return Response(
                {'detail': 'ID do usuário não fornecido.'},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            user = UsuarioManager.get_by_id(user_id)
            if not user:
                return Response(
                    {'detail': 'Usuário não encontrado.'},
                    status=status.HTTP_404_NOT_FOUND
                )
            serializer = UsuarioSerializer(user)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response(
                {'detail': str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )

    @swagger_auto_schema(
        responses={204: 'Usuário deletado com sucesso.'},
        manual_parameters=[
            openapi.Parameter(
                'id', openapi.IN_PATH,
                description="ID do usuário",
                type=openapi.TYPE_STRING
            )
        ],
    )
    def delete(self, request, *args, **kwargs):
        # Verifica se o usuário logado é administrador
        if not request.user.is_staff:
            raise PermissionDenied(
                "Apenas administradores podem deletar usuários."
            )

        user_id = kwargs.get('pk')
        if not user_id:
            return Response(
                {'detail': 'ID do usuário não fornecido.'},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Chama o método do manager para deletar o usuário
        result = UsuarioManager.deletar_usuario(user_id)
        if result['success']:
            return Response(
                {'detail': result['message']},
                status=status.HTTP_204_NO_CONTENT
            )
        else:
            return Response(
                {'detail': result['message']},
                status=status.HTTP_404_NOT_FOUND
            )


class PerfilAPIView(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = PerfilSerializer
    http_method_names = ['get', 'post']

    @swagger_auto_schema(
        responses={200: PerfilSerializer(many=True)},
    )
    def get(self, request):
        perfis = PerfilManager.listar_perfis()
        serializer = PerfilSerializer(perfis, many=True)
        return Response(serializer.data, status=HTTP_200_OK)

    @swagger_auto_schema(
        responses={201: PerfilSerializer(many=False)},
        request_body=PerfilSerializer
    )
    def post(self, request):
        serializer = PerfilSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        try:
            # Criação do perfil associado ao usuário
            usuario = request.user
            perfil = PerfilManager.criar_perfil(
                usuario, serializer.validated_data
            )

            # Serializa e retorna a resposta
            response_serializer = PerfilSerializer(perfil)
            return Response(
                response_serializer.data, status=status.HTTP_201_CREATED
            )

        except Exception as e:
            return Response(
                {'detail': str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )


class PerfilDetailAPIView(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = PerfilSerializer
    http_method_names = ['get', 'put', 'delete']

    @swagger_auto_schema(
        responses={200: PerfilSerializer(many=False)},
        manual_parameters=[
            openapi.Parameter(
                'id', openapi.IN_PATH,
                description="ID do perfil",
                type=openapi.TYPE_INTEGER
            )
        ],
    )
    def get(self, request, *args, **kwargs):
        perfil_id = kwargs.get('pk')
        if not perfil_id:
            return Response(
                {'detail': 'ID do perfil não fornecido.'},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            perfil = PerfilManager.get_by_id(perfil_id)
            if not perfil:
                return Response(
                    {'detail': 'Perfil não encontrado.'},
                    status=status.HTTP_404_NOT_FOUND
                )
            serializer = PerfilSerializer(perfil)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response(
                {'detail': str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )

    @swagger_auto_schema(
        responses={200: PerfilSerializer(many=False)},
        request_body=PerfilSerializer
    )
    def put(self, request, *args, **kwargs):
        perfil_id = kwargs.get('pk')
        if not perfil_id:
            return Response(
                {'detail': 'ID do perfil não fornecido.'},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            perfil = PerfilManager.get_by_id(perfil_id)
            if not perfil:
                return Response(
                    {'detail': 'Perfil não encontrado.'},
                    status=status.HTTP_404_NOT_FOUND
                )

            serializer = PerfilSerializer(
                perfil, data=request.data, partial=True
            )
            serializer.is_valid(raise_exception=True)
            perfil_atualizado = serializer.update(
                perfil, serializer.validated_data
            )

            response_serializer = PerfilSerializer(perfil_atualizado)
            return Response(
                response_serializer.data, status=status.HTTP_200_OK
            )
        except Exception as e:
            return Response(
                {'detail': str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )

    @swagger_auto_schema(
        responses={204: 'Perfil deletado com sucesso.'},
        manual_parameters=[
            openapi.Parameter(
                'id', openapi.IN_PATH,
                description="ID do perfil",
                type=openapi.TYPE_INTEGER
            )
        ],
    )
    def delete(self, request, *args, **kwargs):
        # Verifica se o usuário logado é administrador
        if not request.user.is_staff:
            raise PermissionDenied(
                "Apenas administradores podem deletar perfil."
            )

        perfil_id = kwargs.get('pk')
        if not perfil_id:
            return Response(
                {'detail': 'ID do perfil não fornecido.'},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            result = PerfilManager.deletar_perfil(perfil_id)
            if result['success']:
                return Response(
                    {'detail': result['message']},
                    status=status.HTTP_204_NO_CONTENT
                )
            else:
                return Response(
                    {'detail': result['message']},
                    status=status.HTTP_404_NOT_FOUND
                )
        except Exception as e:
            return Response(
                {'detail': str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )


class EnderecoAPIView(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = EnderecoSerializer
    http_method_names = ['get', 'post']

    @swagger_auto_schema(
        responses={200: EnderecoSerializer(many=True)},
    )
    def get(self, request):
        enderecos = EnderecoManager.listar_enderecos()
        serializer = EnderecoSerializer(enderecos, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @swagger_auto_schema(
        responses={201: EnderecoSerializer(many=False)},
        request_body=EnderecoSerializer
    )
    def post(self, request, **kwargs):
        serializer = EnderecoSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        print("Dados recebidos no request:", request.data)

        try:
            perfil = Perfil.objects.filter(usuario=request.user).first()
            if not perfil:
                return Response(
                    {'detail': 'Perfil não encontrado.'},
                    status=status.HTTP_404_NOT_FOUND
                )

            endereco = EnderecoManager.criar_endereco(
                perfil, serializer.validated_data
            )
            response_serializer = EnderecoSerializer(endereco)
            return Response(
                response_serializer.data, status=status.HTTP_201_CREATED
            )

        except Exception as e:
            return Response(
                {'detail': str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )


class EnderecoDetailAPIView(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = EnderecoSerializer
    http_method_names = ['get', 'put', 'delete']

    @swagger_auto_schema(
        responses={200: EnderecoSerializer(many=False)},
        manual_parameters=[
            openapi.Parameter(
                'id', openapi.IN_PATH,
                description="ID do endereço",
                type=openapi.TYPE_INTEGER
            )
        ],
    )
    def get(self, request, *args, **kwargs):
        endereco_id = kwargs.get('pk')
        if not endereco_id:
            return Response(
                {'detail': 'ID do endereço não fornecido.'},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            endereco = EnderecoManager.get_by_id(endereco_id)
            if not endereco:
                return Response(
                    {'detail': 'Endereço não encontrado.'},
                    status=status.HTTP_404_NOT_FOUND
                )
            serializer = EnderecoSerializer(endereco)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response(
                {'detail': str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )

    @swagger_auto_schema(
        responses={200: EnderecoSerializer(many=False)},
        request_body=EnderecoSerializer
    )
    def put(self, request, *args, **kwargs):
        endereco_id = kwargs.get('pk')
        if not endereco_id:
            return Response(
                {'detail': 'ID do endereço não fornecido.'},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            endereco = EnderecoManager.get_by_id(endereco_id)
            if not endereco:
                return Response(
                    {'detail': 'Endereço não encontrado.'},
                    status=status.HTTP_404_NOT_FOUND
                )

            serializer = EnderecoSerializer(
                endereco, data=request.data, partial=True
            )
            serializer.is_valid(raise_exception=True)
            endereco_atualizado = serializer.update(
                endereco, serializer.validated_data
            )

            response_serializer = EnderecoSerializer(endereco_atualizado)
            return Response(
                response_serializer.data, status=status.HTTP_200_OK
            )
        except Exception as e:
            return Response(
                {'detail': str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )

    @swagger_auto_schema(
        responses={204: 'Endereço deletado com sucesso.'},
        manual_parameters=[
            openapi.Parameter(
                'id', openapi.IN_PATH,
                description="ID do endereço",
                type=openapi.TYPE_INTEGER
            )
        ],
    )
    def delete(self, request, *args, **kwargs):
        # Verifica se o usuário logado é administrador
        if not request.user.is_staff:
            raise PermissionDenied(
                "Apenas administradores podem deletar endereços."
            )

        endereco_id = kwargs.get('pk')
        if not endereco_id:
            return Response(
                {'detail': 'ID do endereço não fornecido.'},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            result = EnderecoManager.deletar_endereco(endereco_id)
            if result['success']:
                return Response(
                    {'detail': result['message']},
                    status=status.HTTP_204_NO_CONTENT
                )
            else:
                return Response(
                    {'detail': result['message']},
                    status=status.HTTP_404_NOT_FOUND
                )
        except Exception as e:
            return Response(
                {'detail': str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )
