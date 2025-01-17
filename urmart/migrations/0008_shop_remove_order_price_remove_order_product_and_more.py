# Generated by Django 5.1.4 on 2024-12-30 04:06

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("urmart", "0007_member_is_vip"),
    ]

    operations = [
        migrations.CreateModel(
            name="Shop",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "name",
                    models.PositiveIntegerField(
                        choices=[(1, "um"), (2, "ms"), (3, "ps")],
                        help_text="商店名稱",
                        unique=True,
                    ),
                ),
            ],
        ),
        migrations.RemoveField(
            model_name="order",
            name="price",
        ),
        migrations.RemoveField(
            model_name="order",
            name="product",
        ),
        migrations.RemoveField(
            model_name="order",
            name="qty",
        ),
        migrations.RemoveField(
            model_name="order",
            name="shop_id",
        ),
        migrations.RemoveField(
            model_name="product",
            name="shop_id",
        ),
        migrations.RemoveField(
            model_name="shopsalesstats",
            name="shop_id",
        ),
        migrations.AddField(
            model_name="product",
            name="name",
            field=models.CharField(default="", max_length=128),
        ),
        migrations.AlterField(
            model_name="member",
            name="member_name",
            field=models.CharField(default="", max_length=128),
        ),
        migrations.CreateModel(
            name="OrderItem",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("qty", models.PositiveIntegerField(default=1, help_text="購買數量")),
                (
                    "price",
                    models.DecimalField(
                        decimal_places=0, default=0, help_text="商品單價", max_digits=10
                    ),
                ),
                (
                    "subtotal",
                    models.DecimalField(
                        decimal_places=0,
                        default=0,
                        editable=False,
                        help_text="小計",
                        max_digits=10,
                    ),
                ),
                (
                    "order",
                    models.ForeignKey(
                        help_text="所屬訂單",
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="items",
                        to="urmart.order",
                    ),
                ),
                (
                    "product",
                    models.ForeignKey(
                        help_text="訂單中的商品",
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="order_items",
                        to="urmart.product",
                    ),
                ),
            ],
        ),
        migrations.AddField(
            model_name="product",
            name="shop",
            field=models.ForeignKey(
                default=1,
                help_text="商品所屬商店",
                on_delete=django.db.models.deletion.CASCADE,
                related_name="products",
                to="urmart.shop",
            ),
        ),
        migrations.AddField(
            model_name="shopsalesstats",
            name="shop",
            field=models.ForeignKey(
                default=1,
                help_text="所屬商店",
                on_delete=django.db.models.deletion.CASCADE,
                related_name="sales_stats",
                to="urmart.shop",
            ),
        ),
    ]
