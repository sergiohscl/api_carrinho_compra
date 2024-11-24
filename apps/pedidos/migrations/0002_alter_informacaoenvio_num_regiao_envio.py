# Generated by Django 5.1.3 on 2024-11-17 19:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pedidos', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='informacaoenvio',
            name='num_regiao_envio',
            field=models.IntegerField(blank=True, choices=[(1, 'Centro-Oeste'), (2, 'Nordeste'), (3, 'Norte'), (4, 'Sudeste'), (5, 'Sul')], default=None, null=True),
        ),
    ]