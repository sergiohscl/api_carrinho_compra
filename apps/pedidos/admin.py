from django.contrib import admin
from .models import InformacaoEnvio, Pedido, DetalhesDoPedido


# TabularInline para DetalhesDoPedido
class DetalhesDoPedidoInline(admin.TabularInline):
    model = DetalhesDoPedido
    extra = 1  # Número de linhas extras exibidas no admin


# Admin para InformacaoEnvio
@admin.register(InformacaoEnvio)
class InformacaoEnvioAdmin(admin.ModelAdmin):
    list_display = (
        'num_envio', 'tipo_envio', 'custo_envio', 'num_regiao_envio'
    )
    search_fields = ('tipo_envio',)
    list_filter = ('num_regiao_envio',)

    def get_num_regiao_envio(self, obj):
        return dict(InformacaoEnvio.REGIAO_CHOICES).get(
            obj.num_regiao_envio, "Não especificada"
        )
    get_num_regiao_envio.short_description = 'Região de Envio'


# Admin para Pedido
@admin.register(Pedido)
class PedidoAdmin(admin.ModelAdmin):
    list_display = (
        'num_pedido', 'cliente', 'estado', 'data_criacao', 'data_envio'
    )
    search_fields = ('num_pedido', 'cliente__user__username', 'estado')
    list_filter = ('estado', 'data_criacao')
    inlines = [DetalhesDoPedidoInline]  # Inclui o TabularInline no admin
