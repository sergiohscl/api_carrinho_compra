from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from apps.carrinho.api.viewsets import ProdutoAPIView, ProdutoDetailAPIView, ProdutoFilterListAPIView # noqa E501
from apps.carrinho.api.viewsets import (
    CarrinhoAPIView, CarrinhoComprasAPIView,  RemoveCarrinhoComprasAPIView,
    AtualizarStatusCarrinhoAPIView, ListarCarrinhosFinalizadosAPIView
)
from apps.pedidos.api.viewsets import InformacaoEnvioAPIView, InformacaoEnvioDetails # noqa E501
from apps.pedidos.api.viewsets import PedidoAPIView, PedidoDetailsAPIView
from apps.perfil.api.viewsets import UsuarioAPIView, UsuarioDetailAPIView
from apps.perfil.api.viewsets import PerfilAPIView,  PerfilDetailAPIView
from apps.perfil.api.viewsets import EnderecoAPIView, EnderecoDetailAPIView


schema_view = get_schema_view(
    openapi.Info(
        title="Snippets API",
        default_version='v1',
        description="Test description",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="contact@snippets.local"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    path('swagger<format>/', schema_view.without_ui(cache_timeout=0),
         name='schema-json'),
    path('swagger/', schema_view.with_ui('swagger',
         cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc',
         cache_timeout=0), name='schema-redoc'),

    path('admin/', admin.site.urls),
    path('usuarios/', UsuarioAPIView.as_view(), name='usuarios'),
    path('usuarios/<int:pk>/', UsuarioDetailAPIView.as_view(), name='usuario-detail'), # noqa E501
    path('perfis/', PerfilAPIView.as_view(), name='perfil-list-create'),
    path('perfis/<int:pk>/', PerfilDetailAPIView.as_view(), name='perfil-detail'), # noqa E501
    path('enderecos/', EnderecoAPIView.as_view(), name='endereco-list-create'),
    path('enderecos/<int:pk>/', EnderecoDetailAPIView.as_view(), name='endereco-detail'), # noqa E501
    path('enderecos/<int:pk>/', EnderecoDetailAPIView.as_view(), name='endereco-detail'), # noqa E501
    path('informacao-envio/', InformacaoEnvioAPIView.as_view(), name='informacao-envio'), # noqa E501
    path('informacao-envio/<int:pk>/', InformacaoEnvioDetails.as_view(), name='informacao-envio-detail'), # noqa E501
    path('pedidos/', PedidoAPIView.as_view(), name='pedidos'),
    path('pedidos/<int:id>/', PedidoDetailsAPIView.as_view(), name='pedido-detail'),  # noqa E501
    path('produtos/', ProdutoAPIView.as_view(), name='produtos'),
    path('produtos/<str:UUID>/', ProdutoDetailAPIView.as_view(), name='produto-detail'), # noqa E501
    path('produtos/filter-list/', ProdutoFilterListAPIView.as_view(), name='produtos-filter-list'), # noqa E501
    path('carrinhos/', CarrinhoAPIView.as_view(), name='carrinhos'),
    path('carrinhos/adicionar/<str:num_produto>/<int:quantidade>/', CarrinhoComprasAPIView.as_view(), name='adicionar-produto-carrinho'),  # noqa E501
    path('carrinhos/remover/<str:nome>/', RemoveCarrinhoComprasAPIView.as_view(), name='remover-produto-carrinho'),  # noqa E501
    path('carrinhos/status/', AtualizarStatusCarrinhoAPIView.as_view(), name='atualizar-status-carrinho'),  # noqa E501
    path('carrinhos/finalizados/', ListarCarrinhosFinalizadosAPIView.as_view(), name='listar-carrinhos-finalizados'), # noqa E501
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL,
                          document_root=settings.STATIC_URL)
