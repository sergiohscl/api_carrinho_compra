from django.contrib.auth.models import User
from apps.perfil.models import Perfil, Endereco


class UsuarioManager:
    @staticmethod
    def criar_usuario(username, email, password):
        user = User.objects.create_user(
            username=username,
            email=email,
            password=password
        )
        return user

    @staticmethod
    def listar_usuarios():
        return User.objects.all()

    @staticmethod
    def get_by_email(email):
        return User.objects.filter(email=email)

    @staticmethod
    def get_by_id(user_id):
        try:
            return User.objects.get(id=user_id)
        except User.DoesNotExist:
            return None

    @staticmethod
    def deletar_usuario(user_id):
        try:
            # Busca o usuário pelo ID
            user = User.objects.get(id=user_id)
            user.delete()
            return {'success': True, 'message': 'Usuário deletado com sucesso.'} # noqa E501
        except User.DoesNotExist:
            return {'success': False, 'message': 'Usuário não encontrado.'}


class PerfilManager:
    @staticmethod
    def criar_perfil(usuario, validated_data):
        perfil = Perfil.objects.create(
            usuario=usuario,
            data_cadastro=validated_data.get('data_cadastro'),
            avatar=validated_data.get('avatar', ''),
            sexo=validated_data.get('sexo', '')
        )
        return perfil

    @staticmethod
    def listar_perfis():
        return Perfil.objects.select_related('usuario').all()

    @staticmethod
    def get_by_id(perfil_id):
        try:
            return Perfil.objects.get(usuario_id=perfil_id)
        except Perfil.DoesNotExist:
            return None

    @staticmethod
    def deletar_perfil(perfil_id):
        try:
            perfil = Perfil.objects.get(id=perfil_id)
            perfil.delete()
            return {'success': True, 'message': 'Perfil deletado com sucesso.'}
        except Perfil.DoesNotExist:
            return {'success': False, 'message': 'Perfil não encontrado.'}


class EnderecoManager:
    @staticmethod
    def criar_endereco(perfil, validated_data):
        endereco = Endereco.objects.create(perfil=perfil, **validated_data)
        print(endereco)
        return endereco

    @staticmethod
    def listar_enderecos():
        return Endereco.objects.select_related('perfil').all()

    @staticmethod
    def get_by_id(endereco_id):
        try:
            return Endereco.objects.get(pk=endereco_id)
        except Endereco.DoesNotExist:
            return None

    @staticmethod
    def deletar_endereco(endereco_id):
        try:
            endereco = Endereco.objects.get(pk=endereco_id)
            endereco.delete()
            return {'success': True, 'message': 'Endereço deletado com sucesso.'} # noqa E501
        except Endereco.DoesNotExist:
            return {'success': False, 'message': 'Endereço não encontrado.'}
