from datetime import datetime

from django.db import models
from django.core.exceptions import ValidationError


# Create your models here.


class Product(models.Model):
    stock_pcs = models.PositiveIntegerField(default=0)
    price = models.DecimalField(max_digits=10, decimal_places=0,default=0)
    shop_choice = ((1, "um"), (2, "ms"), (3, "ps"))
    shop_id = models.PositiveIntegerField(choices=shop_choice, default=1)
    is_vip = models.BooleanField(default=False)

    def __str__(self):
        return f"商品id:{self.id} 庫存:{self.stock_pcs} 價格:{self.price}"


class Member(models.Model):
    member_name = models.CharField(max_length=100, default="")
    is_vip=models.BooleanField(default=False)

    def __str__(self):
        return f"會員號碼 : {self.id} 名字: {self.member_name}"


class Order(models.Model):
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name="orders",
        help_text="購買產品",
        null=True,
        blank=True,
    )
    qty = models.PositiveIntegerField(default=0, help_text="購買數量")
    price = models.DecimalField(
        max_digits=10, decimal_places=0, help_text="商品單價",default=0
    )
    total_price = models.DecimalField(
        max_digits=10, decimal_places=0, default=0, help_text="訂單總額"
    )
    shop_choice = ((1, "um"), (2, "ms"), (3, "ps"))
    shop_id = models.PositiveIntegerField(
        choices=shop_choice, default=1, help_text="商品所屬館別"
    )
    member = models.ForeignKey(
        Member,
        on_delete=models.CASCADE,
        related_name="orders",
        help_text="購買成員",
        null=True,
        blank=True,
    )
    created_at = models.DateTimeField(default=datetime.now)

    def clean(self):
        if not self.product:
            raise ValidationError("需輸入購買的商品")
        if not self.member:
            raise ValidationError("需輸入購買的會員")

    def __str__(self):
        return f"Order:{self.id} (Product:{self.product.id}, Qty:{self.qty})"


class ShopSalesStats(models.Model):
    shop_choice = ((1, "um"), (2, "ms"), (3, "ps"))
    shop_id = models.PositiveIntegerField(choices=shop_choice, default=1)
    total_sales_amount = models.DecimalField(
        max_digits=12, decimal_places=2, default=0
    )
    total_qty = models.PositiveIntegerField(default=0)
    total_orders = models.PositiveIntegerField(default=0)
    date = models.DateField(default=datetime.today)

    def __str__(self):
        return f"Shop id:{self.shop_id} total_sales:{self.total_sales_amount} total_qty:{self.total_qty} total_order:{self.total_orders}  record:{self.date}"
