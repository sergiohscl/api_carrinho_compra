from rest_framework.test import APIClient
from rest_framework import status
from django.urls import reverse
from apps.carrinho.models import Produto
from django.contrib.auth.models import User
from django.test import TestCase


class BaseTestCase(TestCase):
    def setUp(self):
        self.email = "samu@example.com"
        self.name = "samu"
        self.password = "testpassword"
        self.user = User.objects.create_user(
            username=self.name,
            email=self.email,
            password=self.password,
            is_staff=True
        )

        self.client = APIClient()
        self.client.force_authenticate(user=self.user)


class ProdutoAPIViewTest(BaseTestCase):
    def setUp(self):
        super().setUp()
        self.produto_data = {
            "nome": "Produto Teste",
            "descricao": "Descrição do produto teste",
            "preco": 99.99,
            "estoque": 10
        }
        self.produto = Produto.objects.create(**self.produto_data)

    def test_listar_produtos(self):
        url = reverse('produtos')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreaterEqual(len(response.data), 1)

    def test_criar_produto(self):
        url = reverse('produtos')
        produto_data = {
            "nome": "Produto Teste 1",
            "descricao": "Descrição do produto teste 1",
            "preco": 88.88,
            "estoque": 5
        }
        response = self.client.post(url, data=produto_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['nome'], produto_data['nome'])

    def test_detalhar_produto(self):
        url = reverse(
            'produto-detail', kwargs={"UUID": self.produto.num_produto}
        )
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['nome'], self.produto.nome)

    def test_atualizar_produto(self):
        url = reverse(
            'produto-detail', kwargs={"UUID": self.produto.num_produto}
        )
        novo_dado = {"nome": "Produto Atualizado", "descricao": self.produto.descricao, "preco": 79.99, "estoque": 15} # noqa E501
        response = self.client.put(url, data=novo_dado, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['nome'], novo_dado['nome'])

    def test_deletar_produto(self):
        url = reverse(
            'produto-detail', kwargs={"UUID": self.produto.num_produto}
        )
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Produto.objects.filter(
            num_produto=self.produto.num_produto
        ).exists())
