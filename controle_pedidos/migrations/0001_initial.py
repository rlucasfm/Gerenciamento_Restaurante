# Generated by Django 2.2.1 on 2019-06-05 00:17

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='ItensPedido',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cod_pedido', models.PositiveSmallIntegerField(default=0)),
                ('cod_produto', models.PositiveSmallIntegerField(default=0)),
                ('quantidade', models.PositiveSmallIntegerField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='Pedido',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cod_comanda', models.PositiveSmallIntegerField(default=0)),
                ('valor_total', models.DecimalField(decimal_places=2, default=0, max_digits=7)),
                ('pronto', models.BooleanField(default=False)),
                ('pago', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='Produto',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nome', models.CharField(max_length=100)),
                ('valor_unitario', models.DecimalField(decimal_places=2, default=0, max_digits=7)),
                ('descricao', models.CharField(max_length=200)),
            ],
        ),
    ]
