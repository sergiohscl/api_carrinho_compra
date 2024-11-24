from django.test import TestCase
from apps.perfil.models import Endereco, Perfil
from apps.pedidos.models import InformacaoEnvio, Pedido, DetalhesDoPedido
from django.contrib.auth.models import User
from django.utils.timezone import now


class InformacaoEnvioModelTest(TestCase):
    def setUp(self):
        self.info_envio = InformacaoEnvio.objects.create(
            num_envio=1,
            tipo_envio="Entrega Rápida",
            custo_envio=100,
            num_regiao_envio=4,
        )

    def test_info_envio_creation(self):
        self.assertEqual(self.info_envio.num_envio, 1)
        self.assertEqual(self.info_envio.tipo_envio, "Entrega Rápida")
        self.assertEqual(self.info_envio.custo_envio, 100)
        self.assertEqual(self.info_envio.num_regiao_envio, 4)

    def test_info_envio_str(self):
        self.assertEqual(
            str(self.info_envio), "Envio 1 - Tipo: Entrega Rápida"
        )


class PedidoModelTest(TestCase):
    def setUp(self):
        # Criar usuário e perfil
        self.usuario = User.objects.create_user(
            username="cliente_teste",
            email="cliente@mail.com",
            password="senha123"
        )
        self.perfil = Perfil.objects.create(
            usuario=self.usuario,
            data_cadastro=now(),
            sexo=Perfil.Sexo.MASCULINO
        )

        # Criar endereço
        self.endereco = Endereco.objects.create(
            perfil=self.perfil,
            rua="Rua Teste",
            numero="123",
            bairro="Bairro Teste",
            cidade="São Paulo",
            estado="SP",
            cep="12345-678",
            complemento="Apto 101"
        )

        # Criar informação de envio
        self.info_envio = InformacaoEnvio.objects.create(
            num_envio=1,
            tipo_envio="Entrega Normal",
            custo_envio=50,
            num_regiao_envio=3,
        )

        # Criar pedido
        self.pedido = Pedido.objects.create(
            num_pedido=1001,
            cliente=self.perfil,
            estado="Em andamento",
            info_envio=self.info_envio,
        )

    def test_pedido_creation(self):
        self.assertEqual(self.pedido.num_pedido, 1001)
        self.assertEqual(self.pedido.cliente, self.perfil)
        self.assertEqual(self.pedido.estado, "Em andamento")
        self.assertEqual(self.pedido.info_envio, self.info_envio)

    def test_pedido_str(self):
        self.assertEqual(
            str(self.pedido),
            f"Pedido {self.pedido.num_pedido} do cliente {self.perfil}",
        )


class DetalhesDoPedidoModelTest(TestCase):
    def setUp(self):
        # Criar usuário e perfil
        self.usuario = User.objects.create_user(
            username="cliente_detalhe",
            email="cliente_detalhe@mail.com",
            password="senha456"
        )
        self.perfil = Perfil.objects.create(
            usuario=self.usuario,
            data_cadastro=now(),
            sexo=Perfil.Sexo.FEMININO
        )

        # Criar endereço
        self.endereco = Endereco.objects.create(
            perfil=self.perfil,
            rua="Rua Detalhe",
            numero="456",
            bairro="Bairro Detalhe",
            cidade="Rio de Janeiro",
            estado="RJ",
            cep="98765-432",
            complemento="Bloco B"
        )

        # Criar informação de envio
        self.info_envio = InformacaoEnvio.objects.create(
            num_envio=2,
            tipo_envio="Entrega Expressa",
            custo_envio=80,
            num_regiao_envio=5,
        )

        # Criar pedido
        self.pedido = Pedido.objects.create(
            num_pedido=1002,
            cliente=self.perfil,
            estado="Concluído",
            info_envio=self.info_envio,
        )

        # Criar detalhe do pedido
        self.detalhe = DetalhesDoPedido.objects.create(
            pedido=self.pedido,
            num_produto=456,
            nome_produto="Produto Teste 2",
            quantidade=3,
            custo_unidade=30.0,
            subtotal=90.0,
        )

    def test_detalhe_creation(self):
        self.assertEqual(self.detalhe.pedido, self.pedido)
        self.assertEqual(self.detalhe.num_produto, 456)
        self.assertEqual(self.detalhe.nome_produto, "Produto Teste 2")
        self.assertEqual(self.detalhe.quantidade, 3)
        self.assertEqual(self.detalhe.custo_unidade, 30.0)
        self.assertEqual(self.detalhe.subtotal, 90.0)

    def test_detalhe_str(self):
        self.assertEqual(
            str(self.detalhe),
            f"Detalhe do pedido {self.pedido.num_pedido} - Produto: Produto Teste 2", # noqa E501
        )
