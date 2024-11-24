from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
from rest_framework import status

from apps.perfil.models import Endereco, Perfil

User = get_user_model()


class BaseTestCase(TestCase):
    def setUp(self):
        self.email = "samu@example.com"
        self.name = "samu"
        self.password = "testpassword"
        self.user = User.objects.create_user(
            username=self.name, email=self.email, password=self.password
        )

        self.client = APIClient(enforce_csrf_checks=True)
        self.client.force_authenticate(user=self.user)


class UsuarioAPIViewTest(BaseTestCase):
    def test_list_usuarios(self):
        # Testando a listagem de usuarios (GET)
        url = reverse('usuarios')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_list_usuarios_UNAUTHORIZED(self):
        self.client.force_authenticate(user=None)
        url = reverse('usuarios')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_create_usuario(self):
        # Testando a criação de um usuário (POST)
        url = reverse('usuarios')
        data = {
            "username": "novo_user",
            "email": "novo_user@example.com",
            "password": "newpassword123",
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["username"], "novo_user")

    def test_create_usuario_existing_email(self):
        # Testando erro ao criar usuário com e-mail já existente
        url = reverse('usuarios')
        data = {
            "username": "outro_user",
            "email": self.email,
            "password": "otherpassword123",
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("Usuário com este email já existe.", str(response.data))


class UsuarioDetailAPIViewTest(BaseTestCase):
    def test_get_usuario(self):
        # Testando a obtenção de detalhes de um usuário (GET)
        url = reverse('usuario-detail', kwargs={'pk': self.user.id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["username"], self.user.username)

    def test_delete_usuario(self):
        # Testando a exclusão de um usuário (DELETE)
        self.user.is_staff = True
        self.user.save()
        url = reverse('usuario-detail', kwargs={'pk': self.user.id})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_delete_usuario_UNAUTHORIZED(self):
        # Testando exclusão sem permissão
        url = reverse('usuario-detail', kwargs={'pk': self.user.id})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


class PerfilAPIViewTest(BaseTestCase):
    def setUp(self):
        super().setUp()
        self.perfil = Perfil.objects.create(usuario=self.user)

    def test_list_perfis(self):
        # Testando a listagem de perfis (GET)
        url = reverse('perfil-list-create')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_create_perfil(self):
        # Testando a criação de um perfil (POST)
        Perfil.objects.filter(usuario=self.user).delete()

        url = reverse('perfil-list-create')
        data = {
            "data_cadastro": "2024-11-16T14:00:00Z",
            "sexo": "M",
            "usuario": self.user.id
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)


class EnderecoAPIViewTest(BaseTestCase):
    def setUp(self):
        super().setUp()
        self.perfil = Perfil.objects.create(usuario=self.user)
        self.endereco = Endereco.objects.create(
            perfil=self.perfil,
            rua="Rua Exemplo",
            numero="123",
            bairro="Centro",
            cidade="São Paulo",
            estado="SP",
            cep="12345-678",
            complemento="Apto 101",
        )

    def test_list_enderecos(self):
        # Testando a listagem de endereços (GET)
        url = reverse('endereco-list-create')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_create_endereco(self):
        # Testando a criação de um endereço (POST)
        url = reverse('endereco-list-create')
        data = {
            "rua": "Rua Nova",
            "numero": "456",
            "bairro": "Bairro Novo",
            "cidade": "Rio de Janeiro",
            "estado": "RJ",
            "cep": "98765-432",
            "complemento": "Bloco B",
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["rua"], "Rua Nova")


class EnderecoDetailAPIViewTest(BaseTestCase):
    def setUp(self):
        super().setUp()
        self.perfil = Perfil.objects.create(usuario=self.user)
        self.endereco = Endereco.objects.create(
            perfil=self.perfil,
            rua="Rua Exemplo",
            numero="123",
            bairro="Centro",
            cidade="São Paulo",
            estado="SP",
            cep="12345-678",
            complemento="Apto 101",
        )

    def test_get_endereco(self):
        # Testando a obtenção de detalhes de um endereço (GET)
        url = reverse('endereco-detail', kwargs={'pk': self.endereco.id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["rua"], "Rua Exemplo")

    def test_update_endereco(self):
        # Testando a atualização de um endereço (PUT)
        url = reverse('endereco-detail', kwargs={'pk': self.endereco.id})
        data = {"cidade": "Rio de Janeiro", "estado": "RJ"}
        response = self.client.put(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["cidade"], "Rio de Janeiro")

    def test_delete_endereco(self):
        # Testando a exclusão de um endereço (DELETE)
        self.user.is_staff = True
        url = reverse('endereco-detail', kwargs={'pk': self.endereco.id})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
