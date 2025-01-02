# Generated by Django 5.1.4 on 2024-12-30 07:29

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('urmart', '0008_shop_remove_order_price_remove_order_product_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='shopsalesstats',
            name='date',
        ),
        migrations.AddField(
            model_name='shopsalesstats',
            name='created_at',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
        migrations.AlterField(
            model_name='order',
            name='created_at',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
        migrations.AlterField(
            model_name='orderitem',
            name='price',
            field=models.DecimalField(
                decimal_places=0,
                default=0,
                editable=False,
                help_text='商品單價',
                max_digits=10,
            ),
        ),
    ]
