# Generated by Django 5.1.4 on 2024-12-23 05:54

import datetime

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("urmart", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="ShopSalesStats",
            fields=[
                ("id", models.AutoField(primary_key=True, serialize=False)),
                (
                    "shop_id",
                    models.PositiveIntegerField(
                        choices=[(1, "um"), (2, "ms"), (3, "ps")], default=1
                    ),
                ),
                (
                    "total_sales_amount",
                    models.DecimalField(decimal_places=2, default=0, max_digits=12),
                ),
                ("total_qty", models.PositiveIntegerField(default=0)),
                ("total_orders", models.PositiveIntegerField(default=0)),
                ("date", models.DateField(default=datetime.datetime.today)),
            ],
        ),
        migrations.RemoveField(
            model_name="order",
            name="member_id",
        ),
        migrations.AddField(
            model_name="order",
            name="created_at",
            field=models.DateTimeField(default=datetime.datetime.now),
        ),
        migrations.AddField(
            model_name="order",
            name="member",
            field=models.ForeignKey(
                help_text="購買成員",
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="orders",
                to="urmart.member",
            ),
        ),
        migrations.AddField(
            model_name="order",
            name="total_price",
            field=models.DecimalField(
                decimal_places=0, default=0, help_text="訂單總額", max_digits=10
            ),
        ),
        migrations.AlterField(
            model_name="member",
            name="member_name",
            field=models.CharField(default="", max_length=100),
        ),
        migrations.AlterField(
            model_name="order",
            name="price",
            field=models.DecimalField(
                decimal_places=0, help_text="商品單價", max_digits=10
            ),
        ),
        migrations.AlterField(
            model_name="order",
            name="product",
            field=models.ForeignKey(
                help_text="購買產品",
                on_delete=django.db.models.deletion.CASCADE,
                related_name="orders",
                to="urmart.product",
            ),
        ),
        migrations.AlterField(
            model_name="order",
            name="qty",
            field=models.PositiveIntegerField(default=0, help_text="購買數量"),
        ),
        migrations.AlterField(
            model_name="order",
            name="shop_id",
            field=models.PositiveIntegerField(
                choices=[(1, "um"), (2, "ms"), (3, "ps")],
                default=1,
                help_text="商品所屬館別",
            ),
        ),
        migrations.AlterField(
            model_name="product",
            name="is_vip",
            field=models.BooleanField(default=False),
        ),
    ]
