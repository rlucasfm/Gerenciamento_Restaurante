# Generated by Django 2.2.1 on 2019-06-05 16:39

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('controle_pedidos', '0004_auto_20190605_0023'),
    ]

    operations = [
        migrations.AlterField(
            model_name='itenspedido',
            name='cod_produto',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='controle_pedidos.Produto'),
        ),
    ]
