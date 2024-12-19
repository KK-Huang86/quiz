# Generated by Django 5.1.4 on 2024-12-19 06:04

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Member',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('member_name', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('stock_pcs', models.PositiveIntegerField(default=0)),
                ('price', models.DecimalField(decimal_places=0, max_digits=10)),
                ('shop_id', models.PositiveIntegerField(choices=[(1, 'um'), (2, 'ms'), (3, 'ps')], default=1)),
                ('is_vip', models.BooleanField(default=False, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('qty', models.PositiveIntegerField(default=0)),
                ('price', models.DecimalField(decimal_places=0, max_digits=10)),
                ('shop_id', models.PositiveIntegerField()),
                ('member_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='orders', to='Urmart.member')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='orders', to='Urmart.product')),
            ],
        ),
    ]
