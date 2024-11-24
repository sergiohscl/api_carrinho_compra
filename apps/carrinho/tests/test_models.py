from django.test import TestCase
from apps.perfil.models import Perfil
from apps.pedidos.models import InformacaoEnvio
from apps.carrinho.models import Produto, CarrinhoDeCompras
from django.contrib.auth.models import User


class ProdutoCarrinhoTestCase(TestCase):

    def setUp(self):
        # Criando um usuário para associar ao perfil
        self.user = User.objects.create_user(
            username='testuser',
            email='testuser@example.com',
            password='password123',
        )

        self.perfil = Perfil.objects.create(
            usuario=self.user,
            avatar='contas/avatar/test.png',
            sexo=Perfil.Sexo.MASCULINO
        )

        # Criar um produto
        self.produto = Produto.objects.create(
            nome="Produto Teste",
            descricao="Descrição do produto teste",
            preco=99.99,
            estoque=10
        )

        # Criar informações de envio
        self.informacao_envio = InformacaoEnvio.objects.create(
            num_envio=1,
            tipo_envio="Entrega Rápida",
            custo_envio=50.0,
            num_regiao_envio=2
        )

        # Criar um carrinho de compras
        self.carrinho = CarrinhoDeCompras.objects.create(
            cliente=self.perfil,
            itens={
                str(self.produto.id): {
                    "nome": self.produto.nome,
                    "descricao": self.produto.descricao,
                    "preco": self.produto.preco,
                    "quantidade": 2
                }
            },
            frete=self.informacao_envio,
            total=self.produto.preco * 2,
            status=CarrinhoDeCompras.StatusCarrinho.ATIVO
        )

    def test_produto_criacao(self):
        """Testa se o produto foi criado corretamente."""
        self.assertEqual(self.produto.nome, "Produto Teste")
        self.assertEqual(self.produto.preco, 99.99)
        self.assertEqual(self.produto.estoque, 10)

    def test_carrinho_criacao(self):
        """Testa se o carrinho foi criado corretamente."""
        self.assertEqual(self.carrinho.cliente, self.perfil)
        self.assertIn(str(self.produto.id), self.carrinho.itens)
        self.assertEqual(self.carrinho.total, 199.98)
        self.assertEqual(
            self.carrinho.status,
            CarrinhoDeCompras.StatusCarrinho.ATIVO
        )

    def test_carrinho_finalizacao(self):
        """Testa se o carrinho pode ser finalizado."""
        self.carrinho.status = CarrinhoDeCompras.StatusCarrinho.FINALIZADO
        self.carrinho.save()
        self.assertEqual(
            self.carrinho.status,
            CarrinhoDeCompras.StatusCarrinho.FINALIZADO
        )

    def test_carrinho_itens_estrutura(self):
        """Testa a estrutura dos itens no carrinho."""
        itens = self.carrinho.itens
        produto_info = itens.get(str(self.produto.id))
        self.assertIsNotNone(produto_info)
        self.assertEqual(produto_info["nome"], self.produto.nome)
        self.assertEqual(produto_info["quantidade"], 2)

    def test_produto_estoque(self):
        """Testa se o estoque é suficiente para o carrinho."""
        self.assertTrue(self.produto.estoque >= 2)
