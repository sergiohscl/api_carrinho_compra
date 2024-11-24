from django.db import models
from apps.carrinho.models import CarrinhoDeCompras
from apps.pedidos.models import InformacaoEnvio


class CarrinhoManager(models.Manager):
    def criar_carrinho_vazio(self, cliente):

        return CarrinhoDeCompras.objects.create(
            cliente=cliente,
            itens={},
            frete=None,
            total=0.0,
            status=CarrinhoDeCompras.StatusCarrinho.ATIVO
        )

    def add_produto_carrinho(self, carrinho, produto, quantidade):

        itens = carrinho.itens

        # Verifica se há estoque suficiente
        if produto.estoque < quantidade:
            raise ValueError(
                f"Estoque insuficiente para o produto '{produto.nome}'."
            )

        if str(produto.num_produto) in itens:
            itens[str(produto.num_produto)]['quantidade'] += quantidade
            itens[str(produto.num_produto)]['subtotal'] = itens[str(produto.id)]['quantidade'] * produto.preco # noqa E501
        else:
            # Adiciona o produto ao carrinho
            itens[str(produto.num_produto)] = {
                'nome': produto.nome,
                'descricao': produto.descricao,
                'preco': produto.preco,
                'quantidade': quantidade,
                'subtotal': quantidade * produto.preco,
            }

        # Decrementa o estoque do produto
        produto.estoque -= quantidade
        produto.save()

        # Recalcula o total do carrinho
        carrinho.itens = itens
        carrinho.total = sum(item['subtotal'] for item in itens.values())
        carrinho.save()
        return carrinho

    def get_carrinho_ativo(self, cliente):

        return CarrinhoDeCompras.objects.filter(
            cliente=cliente,
            status=CarrinhoDeCompras.StatusCarrinho.ATIVO
        ).first()

    def obter_custo_frete(self, carrinho):

        if carrinho.frete:
            return carrinho.frete.custo_envio
        return 0.0

    def calcular_total_com_frete(self, carrinho):

        subtotal = sum(
            item['preco'] * item['quantidade'] for item in carrinho.itens.values() # noqa E501
        )
        custo_frete = self.obter_custo_frete(carrinho)
        carrinho.total = subtotal + custo_frete
        carrinho.save()
        return carrinho.total

    def atribuir_frete(self, carrinho, informacao_envio_id):

        try:
            frete = InformacaoEnvio.objects.get(id=informacao_envio_id)
            carrinho.frete = frete
            carrinho.save()
        except InformacaoEnvio.DoesNotExist:
            raise ValueError("Informação de envio não encontrada.")
        return carrinho
