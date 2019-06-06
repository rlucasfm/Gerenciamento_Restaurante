from django.db import models
from datetime import date

# Create your models here.
class Produto(models.Model):
    nome = models.CharField(max_length=100)
    valor_unitario = models.DecimalField(default=0, max_digits=7, decimal_places=2)
    descricao = models.CharField(max_length=200)

    def cod_produto(self):
        return self.pk

    def __str__(self):
        return self.nome

class Pedido(models.Model):
    cod_comanda = models.PositiveSmallIntegerField(default=0, primary_key=True)
    valor_total = models.DecimalField(default=0, max_digits=7, decimal_places=2)
    pago = models.BooleanField(default=False)
    data = models.DateField(default=date.today)
    cod_mesa = models.PositiveSmallIntegerField(default=0)

    def __str__(self):
        return ("Código da Comanda:"+str(self.cod_comanda))

class ItensPedido(models.Model):
    cod_pedido = models.PositiveSmallIntegerField(default=0)
    cod_produto = models.PositiveSmallIntegerField(default=0)
    quantidade = models.SmallIntegerField(default=0)

    def __str__(self):
        return ("Cod_Pedido:"+str(self.cod_pedido)+" Produto:"+str(self.cod_produto)+", Qnt:"+str(self.quantidade))