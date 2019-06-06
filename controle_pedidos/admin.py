from django.contrib import admin
from .models import  Produto, ItensPedido, Pedido

# Register your models here.
admin.site.register(Produto)
admin.site.register(ItensPedido)
admin.site.register(Pedido)