from rest_framework import serializers
from apps.perfil.models import Perfil
from django.contrib.auth import get_user_model

User = get_user_model()


class UsuarioSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    username = serializers.CharField(max_length=150)
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True, min_length=8)


class EnderecoSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    rua = serializers.CharField(max_length=255)
    numero = serializers.CharField(max_length=10)
    bairro = serializers.CharField(max_length=100)
    cidade = serializers.CharField(max_length=100)
    estado = serializers.CharField(max_length=2)
    cep = serializers.CharField(max_length=9)
    complemento = serializers.CharField(
        max_length=255, required=False, allow_blank=True
    )


class PerfilSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    usuario = serializers.CharField(source='usuario.username', read_only=True)
    data_cadastro = serializers.DateTimeField()
    avatar = serializers.ImageField(allow_null=True, required=False)
    sexo = serializers.ChoiceField(
        choices=Perfil.Sexo.choices, allow_blank=True, required=False
    )
    enderecos = EnderecoSerializer(many=True, read_only=True)
