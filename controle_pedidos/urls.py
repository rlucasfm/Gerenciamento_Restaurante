from django.urls import path
from . import views

app_name = 'controle_pedidos'
urlpatterns = [
    path('', views.Login, name="login"),
    path('idcomanda', views.IDComanda, name="idcomanda"),
    path('logout', views.Logout, name='logout'),
    path('menu', views.Menu, name='menu'),
    path('idcomanda/<int:id>', views.DetalhesPedido, name='detalhespedido'),
    path('novopedido/<int:id>', views.NovoPedido, name='novopedido'),
    path('idcomandagerencia/<int:id>', views.DetalhesGerencia, name='detalhespedidogerencia'),
    path('gerenciaprodutos', views.GerenciaProdutos, name='gerenciaprodutos'),
    path('gerenciaprodutos/detalhes/<int:id>', views.DetalhesProduto, name='detalhesproduto'),
    path('gerenciaprodutos/adicionar', views.AdicionarProduto, name='adicionarproduto'),
    path('listapedidos', views.ListaPedidos, name='listapedidos'),
]