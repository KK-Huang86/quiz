from datetime import datetime

from django.db import models
from django.core.exceptions import ValidationError


# Create your models here.


class Shop(models.Model):
    SHOP_CHOICES = (
        (1, "um"),
        (2, "ms"),
        (3, "ps"),
    )
    name = models.PositiveIntegerField(choices=SHOP_CHOICES, unique=True, help_text="商店名稱")

class Product(models.Model):
    name = models.CharField(max_length=128,default='')
    stock_pcs = models.PositiveIntegerField(default=0)
    price = models.DecimalField(max_digits=10, decimal_places=0,default=0)
    shop = models.ForeignKey(Shop,on_delete=models.CASCADE,related_name='products',help_text='商品所屬商店',default=1)
    is_vip = models.BooleanField(default=False)

    def __str__(self):
        return f'商品id:{self.id} 庫存:{self.stock_pcs} 價格:{self.price}'


class Member(models.Model):
    member_name = models.CharField(max_length=128, default='')
    is_vip=models.BooleanField(default=False)

    def __str__(self):
        return f'會員號碼 : {self.id} 名字: {self.member_name} 是否為vip:{str(self.is_vip)}'


class Order(models.Model):
    total_price = models.DecimalField(
        max_digits=10, decimal_places=0, default=0, help_text='訂單總額'
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
        if not self.member:
            raise ValidationError("需輸入購買的會員")

    def calculate_total_price(self):
        """計算訂單的總價格"""
        self.total_price = sum(item.subtotal for item in self.items.all())
        self.save()

    # def __str__(self):
    #     return f"Order:{self.id} (Product:{self.product.id}, Qty:{self.qty})"


class OrderItem(models.Model):
  order = models.ForeignKey(Order,
        on_delete=models.CASCADE,
        related_name="items",
        help_text="所屬訂單",
    )

  product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name="order_items",
        help_text="訂單中的商品",
    )
  qty = models.PositiveIntegerField(default=1, help_text="購買數量")
  price = models.DecimalField(max_digits=10, decimal_places=0,default=0,help_text="商品單價")
  subtotal = models.DecimalField(
        max_digits=10, decimal_places=0, help_text="小計", editable=False,default=0
    )

  def save(self, *args, **kwargs):
        """計算小計"""
        self.subtotal = self.qty * self.price
        super().save(*args, **kwargs)

class ShopSalesStats(models.Model):
    shop =models.ForeignKey(Shop,on_delete=models.CASCADE,related_name='sales_stats',help_text='所屬商店',default=1)
    total_sales_amount = models.DecimalField(
        max_digits=12, decimal_places=2, default=0
    )
    total_qty = models.PositiveIntegerField(default=0)
    total_orders = models.PositiveIntegerField(default=0)
    date = models.DateField(default=datetime.today)

    def __str__(self):
        return f"Shop id:{self.shop_id} total_sales:{self.total_sales_amount} total_qty:{self.total_qty} total_order:{self.total_orders}  record:{self.date}"
