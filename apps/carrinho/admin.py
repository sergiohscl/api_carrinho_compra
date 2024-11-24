from django.contrib import admin
from .models import CarrinhoDeCompras, Produto


@admin.register(Produto)
class ProdutoAdmin(admin.ModelAdmin):
    list_display = ('id', 'nome', 'preco', 'estoque')
    search_fields = ('nome',)
    list_filter = ('preco',)
    ordering = ('nome',)


@admin.register(CarrinhoDeCompras)
class CarrinhoDeComprasAdmin(admin.ModelAdmin):
    list_display = ('id', 'cliente', 'total', 'status')
    list_filter = ('status',)
    search_fields = (
        'cliente__first_name', 'cliente__last_name', 'cliente__email'
    )
    readonly_fields = ('total',)
    fieldsets = (
        ('Informações do Cliente', {
            'fields': ('cliente',)
        }),
        ('Detalhes do Carrinho', {
            'fields': ('itens', 'frete', 'total', 'status')
        }),
    )
    ordering = ('-id',)

    def has_add_permission(self, request):
        """Impede a criação de carrinhos diretamente no admin."""
        return False
