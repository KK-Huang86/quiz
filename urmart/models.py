from datetime import datetime

from django.core.exceptions import ValidationError
from django.db import models, transaction
from django.utils import timezone
import logging
from decimal import Decimal


logger = logging.getLogger('django')
logger.info("錯誤")
de_zero = Decimal('0.00')


# Create your models here.



class Shop(models.Model):
    SHOP_CHOICES = (
        (1, 'um'),
        (2, 'ms'),
        (3, 'ps'),
    )
    name = models.PositiveIntegerField(
        choices=SHOP_CHOICES, unique=True, help_text='商店名稱'
    )

    def __str__(self):
        return f'商店id {self.id} 商店名稱 {self.get_name_display()}'


class Product(models.Model):
    name = models.CharField(max_length=128, default='')
    stock_pcs = models.PositiveIntegerField(default=0)
    price = models.DecimalField(max_digits=10, decimal_places=0, default=0)
    shop = models.ForeignKey(
        Shop,
        on_delete=models.SET_NULL,
        related_name='products',
        help_text='商品所屬商店',
        null=True,
        blank=True,
    )
    is_vip = models.BooleanField(default=False)

    def __str__(self):
        return f"商品id:{self.id} 庫存:{self.stock_pcs} 價格:{self.price} 商店:{self.shop.name}"


class Member(models.Model):
    member_name = models.CharField(max_length=128, default="")
    is_vip = models.BooleanField(default=False)

    def __str__(self):
        return f'會員號碼 : {self.id} 名字: {self.member_name} 是否為vip:{str(self.is_vip)}'


class Order(models.Model):
    total_price = models.DecimalField(
        max_digits=10, decimal_places=0, default=de_zero, help_text='訂單總額'
    )
    member = models.ForeignKey(
        Member,
        on_delete=models.SET_NULL,
        related_name='orders',
        help_text='購買成員',
        null=True,
        blank=True,
    )
    created_at = models.DateTimeField(default=timezone.now)

    def clean(self):
        if not self.member:
            raise ValidationError('需輸入購買的會員')

    def calculate_total_price(self):
        """計算訂單的總價格"""
        self.total_price = sum(item.subtotal for item in self.items.all())
        self.save()

    def __str__(self):
        return f'訂購編號id:{self.id}, 會員id:{self.member.id},訂購商品:{self.order_items}.:{self.total_price}'


class OrderItem(models.Model):
    order = models.ForeignKey(
        Order,
        on_delete=models.SET_NULL,
        related_name='items',
        help_text='所屬訂單',
        null=True,
        blank=True,
    )

    product = models.ForeignKey(
        Product,
        on_delete=models.DO_NOTHING,
        related_name='order_items',
        help_text='訂單中的商品',
    )
    qty = models.PositiveIntegerField(default=1, help_text='購買數量')
    price = models.DecimalField(
        max_digits=10, decimal_places=0, default=de_zero, help_text='商品單價', editable=False
    )

    @property
    def subtotal(self):
        if self.product and self.qty:
            if self.product.price >0 and self.qty > 0:
                return self.product.price * self.qty
        logger.info(f"錯誤的小計金額 OrderItem {self.id}. Price: {self.product.price}, Qty: {self.qty}")
        return 0


    def save(self, *args, **kwargs):
        with transaction.atomic():
            # 找尋原有的庫存數量
            if self.pk:
                old_order_item = OrderItem.objects.get(pk=self.pk)
                old_order_item.adjust_stock(old_order_item.qty)
            # 計算子訂單價格
            self.price = self.product.price
            self.adjust_stock(-self.qty)
            super().save(*args, **kwargs)
            # 同時更新總金額
            self.order.calculate_total_price()

    # def adjust_stock_and_calculate(self):
    #     self.price = self.product.price
    #     self.subtotal = self.qty * self.price
    #     self.product.stock_pcs -= self.qty
    #     self.product.save()

    def delete(self, *args, **kwargs):
        self.adjust_stock(self.qty)
        super().delete(*args, **kwargs)
        self.order.calculate_total_price()

    def adjust_stock(self, qty):
        self.product.stock_pcs += qty
        self.product.save()

    def __str__(self):
        return f'Order:{self.id}, Product:{self.product.id}, Qty:{self.qty} , Price:{self.price} , Subtotal:{self.subtotal}'


class ShopSalesStats(models.Model):
    shop = models.ForeignKey(
        Shop,
        on_delete=models.SET_NULL,
        related_name='sales_stats',
        help_text='所屬商店',
        null=True,
        blank=True,
    )
    total_sales_amount = models.DecimalField(max_digits=12, decimal_places=2, default=de_zero)
    total_qty = models.PositiveIntegerField(default=0)
    total_orders = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f'Shop id:{self.shop_id}, total_sales:{self.total_sales_amount}, total_qty:{self.total_qty}, total_order:{self.total_orders}, record:{self.created_at}'
