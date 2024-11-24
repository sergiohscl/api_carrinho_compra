from django.db import models


class ProdutosManager(models.Manager):

    def criar_produto(self, nome, descricao, preco, estoque):

        if preco <= 0:
            raise ValueError("O preço do produto deve ser maior que zero.")
        if estoque < 0:
            raise ValueError("O estoque não pode ser negativo.")

        produto = self.create(
            nome=nome,
            descricao=descricao,
            preco=preco,
            estoque=estoque
        )
        return produto

    def get_by_uuid(self, model, produto_uuid):

        if not produto_uuid:
            raise ValueError("O UUID do produto é obrigatório.")

        try:
            return model.objects.get(num_produto=produto_uuid)
        except model.DoesNotExist:
            raise model.DoesNotExist("Produto não encontrado.")

    def validate_update(self, data):

        if 'price' in data and data['price'] < 0:
            raise ValueError("O preço do produto não pode ser negativo.")
        return True

    def update_produto(self, model, produto_uuid, data):

        produto = self.get_by_uuid(model, produto_uuid)
        if self.validate_update(data):
            for key, value in data.items():
                setattr(produto, key, value)
            produto.save()
            return produto

    def delete_produto(self, model, produto_uuid):

        produto = self.get_by_uuid(model, produto_uuid)
        produto.delete()
        return True
