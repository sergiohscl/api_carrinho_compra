# Generated by Django 5.1.3 on 2024-11-17 15:15

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('perfil', '0002_endereco'),
    ]

    operations = [
        migrations.CreateModel(
            name='InformacaoEnvio',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('num_envio', models.IntegerField(unique=True)),
                ('tipo_envio', models.CharField(max_length=50)),
                ('custo_envio', models.IntegerField()),
                ('num_regiao_envio', models.IntegerField()),
            ],
            options={
                'verbose_name': 'Informação de Envio',
                'verbose_name_plural': 'Informações de Envio',
            },
        ),
        migrations.CreateModel(
            name='Pedido',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('num_pedido', models.IntegerField(unique=True)),
                ('data_criacao', models.DateTimeField(auto_now_add=True)),
                ('data_envio', models.DateTimeField(blank=True, null=True)),
                ('estado', models.CharField(max_length=50)),
                ('cliente', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='perfil.perfil')),
                ('info_envio', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='pedidos.informacaoenvio')),
            ],
            options={
                'verbose_name': 'Pedido',
                'verbose_name_plural': 'Pedidos',
            },
        ),
        migrations.CreateModel(
            name='DetalhesDoPedido',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('num_produto', models.IntegerField()),
                ('nome_produto', models.CharField(max_length=100)),
                ('quantidade', models.IntegerField()),
                ('custo_unidade', models.FloatField()),
                ('subtotal', models.FloatField()),
                ('pedido', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='pedidos.pedido')),
            ],
            options={
                'verbose_name': 'Detalhe do Pedido',
                'verbose_name_plural': 'Detalhes do Pedido',
            },
        ),
    ]
