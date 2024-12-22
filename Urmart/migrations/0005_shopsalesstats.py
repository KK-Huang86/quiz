# Generated by Django 5.1.4 on 2024-12-22 05:52

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Urmart', '0004_alter_product_is_vip'),
    ]

    operations = [
        migrations.CreateModel(
            name='ShopSalesStats',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('shop_id', models.PositiveIntegerField(choices=[(1, 'um'), (2, 'ms'), (3, 'ps')], default=1)),
                ('total_sales_amount', models.DecimalField(decimal_places=2, max_digits=12)),
                ('total_qty', models.PositiveIntegerField(default=0)),
                ('total_orders', models.PositiveIntegerField(default=0)),
                ('date', models.DateField(default=datetime.datetime.today)),
            ],
        ),
    ]
