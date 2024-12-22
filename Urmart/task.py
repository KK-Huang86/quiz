import datetime
from os import stat

from celery import Celery, shared_task
from .models import  ShopSalesStats,Order
from django.db import models
from django.db.models import Sum, Count,F
from django.db.models.functions import Cast

app = Celery("Urmart")


@shared_task()
def test_task():
    print("---------這是測試，測試成功-------{id}，")

@shared_task()
def generate_shop_sales_stats():
    today = datetime.date.today()  # 抓出符合當天的訂單資料
    shop_stats = (
        Order.objects.filter(created_at__date=today).values('shop_id').annotate(
            total_sales_amount=Sum(Cast(F('qty'), models.DecimalField()) * Cast(F('price'), models.DecimalField())),
            total_qty=Count('qty'),
            total_orders=Count('id')
        )
    )

    '''
    shop_stats的資料類型
    [
    {'shop_id': 1, 'total_sales_amount': 100.0, 'total_qty': 5, 'total_orders': 3},
    {'shop_id': 2, 'total_sales_amount': 150.0, 'total_qty': 6, 'total_orders': 4}
    ]
    
    or 
    shop_stats,<class 'django.db.models.query.QuerySet'>,<QuerySet [{'shop_id': 1, 'total_sales_amount': Decimal('9497280'), 'total_qty': 26, 'total_orders': 26}, {'shop_id': 2, 'total_sales_amount': Decimal('10626640'), 'total_qty': 8, 'total_orders': 8}]>

    '''
    print(f"shop_stats,{type(shop_stats)},{shop_stats}")
    # value 抓出來會是 dict 的形式

    for stat in shop_stats:
        shop_id=stat['shop_id']
        total_sales_amount=stat['total_sales_amount'] or 0
        total_qty=stat['total_qty'] or 0
        total_orders=stat['total_orders'] or 0

        # 如果該日期已經有記錄，則更新，否則創建新記錄
        ShopSalesStats.objects.update_or_create(
            shop_id=shop_id,date=today,
            defaults={
            'total_sales_amount':total_sales_amount,
            'total_qty':total_qty,
            'total_orders':total_orders
            }
        )
        print(f"Shop {shop_id}: Sales={total_sales_amount}, Qty={total_qty}, Orders={total_orders}")
