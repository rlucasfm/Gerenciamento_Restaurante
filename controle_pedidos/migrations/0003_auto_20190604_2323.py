# Generated by Django 2.2.1 on 2019-06-05 02:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('controle_pedidos', '0002_pedido_data'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='pedido',
            name='id',
        ),
        migrations.AlterField(
            model_name='pedido',
            name='cod_comanda',
            field=models.PositiveSmallIntegerField(default=0, primary_key=True, serialize=False),
        ),
    ]
