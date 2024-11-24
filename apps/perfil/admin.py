from django.contrib import admin
from .models import Endereco, Perfil


@admin.register(Perfil)
class PerfilAdmin(admin.ModelAdmin):
    list_display = ('usuario', 'data_cadastro', 'sexo')
    search_fields = ('usuario__username', 'sexo')
    list_filter = ('sexo', 'data_cadastro')
    ordering = ('data_cadastro',)

    def get_avatar(self, obj):
        if obj.avatar:
            return obj.avatar.url
        return "No avatar"
    get_avatar.short_description = "Avatar"


@admin.register(Endereco)
class EnderecoAdmin(admin.ModelAdmin):
    list_display = ('perfil', 'rua', 'numero', 'bairro', 'cidade', 'estado', 'cep') # noqa E501
    search_fields = ('perfil__usuario__username', 'cidade', 'estado', 'cep')
    list_filter = ('cidade', 'estado')
    ordering = ('cidade',)

    def perfil_usuario(self, obj):
        return obj.perfil.usuario.username
    perfil_usuario.short_description = 'Usuário'
