# Generated by Django 5.1.4 on 2024-12-17 08:00

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('stock_pcs', models.PositiveIntegerField(default=0)),
                ('price', models.DecimalField(decimal_places=0, max_digits=10)),
                ('shop_id', models.PositiveIntegerField()),
                ('is_vip', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('qty', models.PositiveIntegerField(default=0)),
                ('price', models.DecimalField(decimal_places=0, max_digits=10)),
                ('shop_id', models.PositiveIntegerField()),
                ('customer_id', models.PositiveIntegerField()),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Urmart.product')),
            ],
        ),
    ]