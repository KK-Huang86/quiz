from django.db import models

# Create your models here.

class Product(models.Model):
    id = models.AutoField(primary_key=True)
    stock_pcs=models.PositiveIntegerField(default=0)
    price = models.DecimalField(max_digits=10, decimal_places=0)
    shop_id = models.PositiveIntegerField()
    is_vip = models.BooleanField(default=False)

    def __str__(self):
        return f"Product:{self.id} Stock:{self.stock_pcs} Price:{self.price}"

class Order(models.Model):
    id = models.AutoField(primary_key=True)
    product=models.ForeignKey(Product, on_delete=models.CASCADE)
    qty=models.PositiveIntegerField(default=0)
    price=models.DecimalField(max_digits=10, decimal_places=0)
    shop_id = models.PositiveIntegerField()
    customer_id = models.PositiveIntegerField()

    def __str__(self):
        return f"Order:{self.id} (Product:{self.product.id}, Qty:{self.qty})"