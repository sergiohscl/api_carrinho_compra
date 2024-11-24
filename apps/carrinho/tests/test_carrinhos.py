from rest_framework.test import APIClient
from rest_framework import status
from django.urls import reverse
from apps.carrinho.models import Produto, CarrinhoDeCompras
from apps.perfil.models import Endereco, Perfil
from apps.pedidos.models import InformacaoEnvio
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


class CarrinhoAPIViewTest(BaseTestCase):
    def setUp(self):
        super().setUp()
        self.perfil = Perfil.objects.create(
            usuario=self.user,
            sexo=Perfil.Sexo.MASCULINO
        )
        self.endereco = Endereco.objects.create(
            perfil=self.perfil,
            estado='SP',  # Estado para teste
            cidade='São Paulo',
            rua='Rua Teste',
            numero='123',
            cep='01234-567'
        )
        self.produto = Produto.objects.create(
            id=1,
            num_produto='2edc82f1-5ec4-493d-b29f-6786cd0e67e7',
            nome="Produto Teste",
            descricao="Descrição do produto",
            preco=99.99,
            estoque=10
        )
        self.informacao_envio = InformacaoEnvio.objects.create(
            num_envio=1,
            tipo_envio="Entrega Normal",
            custo_envio=10.0,
            num_regiao_envio=1
        )
        self.carrinho = CarrinhoDeCompras.objects.create(
            cliente=self.perfil,
            itens={},
            total=0.0,
            status=CarrinhoDeCompras.StatusCarrinho.ATIVO
        )

    def test_listar_carrinhos_ativos(self):
        url = reverse('carrinhos')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreaterEqual(len(response.data), 1)

    def test_criar_carrinho(self):
        url = reverse('carrinhos')
        response = self.client.post(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['cliente'], self.perfil.pk)

    def test_adicionar_produto_com_estoque_insuficiente(self):
        url = reverse(
            'adicionar-produto-carrinho',
            kwargs={"num_produto": str(self.produto.num_produto), "quantidade": 15} # noqa E501
        )
        response = self.client.post(url, format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("Estoque insuficiente", response.data['detail'])

    def test_adicionar_produto_ao_carrinho(self):
        quantidade = 2

        self.assertLessEqual(
            quantidade, self.produto.estoque, "Estoque insuficiente"
        )
        self.informacao_envio.num_regiao_envio = 4
        self.informacao_envio.save()

        url = reverse(
            'adicionar-produto-carrinho',
            kwargs={
                "num_produto": str(self.produto.num_produto),
                "quantidade": quantidade
            }
        )
        response = self.client.post(url, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn(
            str(self.produto.num_produto),
            response.data['carrinho']['itens']
        )
        esperado_total = quantidade * self.produto.preco + self.informacao_envio.custo_envio # noqa E501
        self.assertEqual(response.data['carrinho']['total'], esperado_total)

    def test_remover_produto_do_carrinho(self):
        self.carrinho.itens = {
            str(self.produto.nome): {
                "nome": self.produto.nome,
                "descricao": self.produto.descricao,
                "preco": self.produto.preco,
                "quantidade": 2
            }
        }
        self.carrinho.save()

        url = reverse(
            'remover-produto-carrinho',
            kwargs={"nome": self.produto.nome}
        )
        response = self.client.delete(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.carrinho.refresh_from_db()
        self.assertEqual(
            self.carrinho.itens[str(self.produto.nome)]['quantidade'], 2
        )

    def test_finalizar_carrinho(self):
        url = reverse('atualizar-status-carrinho')
        response = self.client.patch(url, data={"status": "F"}, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.carrinho.refresh_from_db()
        self.assertEqual(
            self.carrinho.status, CarrinhoDeCompras.StatusCarrinho.FINALIZADO
        )
