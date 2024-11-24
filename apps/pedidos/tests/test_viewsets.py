from django.test import TestCase
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
from rest_framework import status
from django.urls import reverse
from apps.pedidos.models import InformacaoEnvio, Pedido
from apps.perfil.models import Perfil, Endereco

User = get_user_model()


class BaseTestCase(TestCase):
    def setUp(self):
        # Criação de um usuário comum
        self.user = User.objects.create_user(
            username="testuser",
            email="testuser@example.com",
            password="password123"
        )

        # Criação de perfil associado ao usuário
        self.perfil = Perfil.objects.create(usuario=self.user)

        # Criação de endereço associado ao perfil
        self.endereco = Endereco.objects.create(
            perfil=self.perfil,
            rua="Rua Exemplo",
            numero="123",
            bairro="Centro",
            cidade="São Paulo",
            estado="SP",
            cep="12345-678",
            complemento="Apto 101"
        )

        self.client = APIClient(enforce_csrf_checks=True)
        self.client.force_authenticate(user=self.user)


class PedidoViewSetTest(BaseTestCase):
    def setUp(self):
        super().setUp()
        # Criar informações de envio para os testes
        self.info_envio = InformacaoEnvio.objects.create(
            num_envio=1, tipo_envio="Expresso",
            custo_envio=50, num_regiao_envio=4
        )

    def test_list_pedidos(self):
        # Criando um pedido para testar a listagem
        Pedido.objects.create(
            num_pedido=1, cliente=self.perfil, estado="SP",
            info_envio=self.info_envio
        )

        url = reverse('pedidos')
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_create_pedido(self):
        url = reverse('pedidos')
        data = {
            "num_pedido": 2,
            "info_envio": self.info_envio.id,
            "detalhes": [
                {
                    "num_produto": 101,
                    "nome_produto": "Produto Teste",
                    "quantidade": 2,
                    "custo_unidade": 25.00,
                    "subtotal": 50.00
                }
            ]
        }
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["num_pedido"], 2)


class InformacaoEnvioViewSetTest(BaseTestCase):
    def test_list_informacoes_envio(self):
        # Criando uma informação de envio para testar a listagem
        InformacaoEnvio.objects.create(
            num_envio=1,
            tipo_envio="Normal",
            custo_envio=20,
            num_regiao_envio=1
        )
        url = reverse('informacao-envio')
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_create_informacao_envio(self):
        url = reverse('informacao-envio')
        data = {
            "num_envio": 2,
            "tipo_envio": "Expresso",
            "custo_envio": 50,
            "num_regiao_envio": 4
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["tipo_envio"], "Expresso")

    def test_update_informacao_envio(self):
        info_envio = InformacaoEnvio.objects.create(
            num_envio=3,
            tipo_envio="Normal",
            custo_envio=30,
            num_regiao_envio=3
        )
        url = reverse('informacao-envio-detail', kwargs={'pk': info_envio.id})
        data = {
            "num_envio": 3,
            "tipo_envio": "Ultra Expresso",
            "custo_envio": 30,
            "num_regiao_envio": 3
        }
        response = self.client.put(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["tipo_envio"], "Ultra Expresso")

    def test_delete_informacao_envio(self):
        info_envio = InformacaoEnvio.objects.create(
            num_envio=4,
            tipo_envio="Normal",
            custo_envio=25,
            num_regiao_envio=2
        )
        url = reverse('informacao-envio-detail', kwargs={'pk': info_envio.id})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
