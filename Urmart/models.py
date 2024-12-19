from django.db import models

# Create your models here.

class Product(models.Model):
    id = models.AutoField(primary_key=True)
    stock_pcs=models.PositiveIntegerField(default=0,null=False)
    price = models.DecimalField(max_digits=10, decimal_places=0,null=False)
    shop_choice=(
        (1,"um"),
        (2,"ms"),
        (3,"ps")
    )
    shop_id = models.PositiveIntegerField(choices=shop_choice,default=1)
    is_vip = models.BooleanField(default=False,null=True)

    def __str__(self):
        return f"商品id:{self.id} 庫存:{self.stock_pcs} 價格:{self.price}"

class Member(models.Model):
    id = models.AutoField(primary_key=True)
    member_name = models.CharField(max_length=100,null=False)

    def __str__(self):
        return f"會員號碼 : {self.id} 名字: {self.member_name}"

class Order(models.Model):
    id = models.AutoField(primary_key=True)
    product=models.ForeignKey(Product, on_delete=models.CASCADE, related_name='orders',null=False)
    qty=models.PositiveIntegerField(default=0,null=False)
    price=models.DecimalField(max_digits=10, decimal_places=0,null=False)
    shop_choice = (
        (1, "um"),
        (2, "ms"),
        (3, "ps")
    )
    shop_id = models.PositiveIntegerField(choices=shop_choice,default=1)
    member=models.ForeignKey(Member, on_delete=models.CASCADE, related_name='orders',null=False)

    def __str__(self):
        return f"Order:{self.id} (Product:{self.product.id}, Qty:{self.qty})"