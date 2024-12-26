import csv
from datetime import datetime,timedelta
import os
from os import stat

from celery import Celery, shared_task
from django.db import models
from django.db.models import Count, F, Sum
from django.db.models.functions import Cast

from .models import Order, ShopSalesStats

app = Celery("Urmart")


@shared_task()
def test_task(id):
    print("---------這是測試，測試成功-------{id}，")


@shared_task()
def generate_shop_sales_stats():
    today = datetime.now().date()
    yesterday = today - timedelta(days=1) #抓出昨天的銷售資料
    shop_stats = (
        Order.objects.filter(created_at__date=yesterday)
        .values("shop_id")
        .annotate(
            total_sales_amount=Sum(
                Cast(F("qty"), models.DecimalField())
                * Cast(F("price"), models.DecimalField())
            ),
            total_qty=Sum("qty"),
            total_orders=Count("id"),
        )
    )

    """
    shop_stats的資料類型
    [
    {'shop_id': 1, 'total_sales_amount': 100.0, 'total_qty': 5, 'total_orders': 3},
    {'shop_id': 2, 'total_sales_amount': 150.0, 'total_qty': 6, 'total_orders': 4}
    ]

    or
    shop_stats,<class 'django.db.models.query.QuerySet'>,<QuerySet [{'shop_id': 1, 'total_sales_amount': Decimal('9497280'), 'total_qty': 26, 'total_orders': 26}, {'shop_id': 2, 'total_sales_amount': Decimal('10626640'), 'total_qty': 8, 'total_orders': 8}]>

    """
    print(f"shop_stats,{type(shop_stats)},{shop_stats}")
    # value 抓出來會是 dict 的形式

    for stat in shop_stats:
        shop_id = stat["shop_id"]
        total_sales_amount = stat["total_sales_amount"] or 0
        total_qty = stat["total_qty"] or 0
        total_orders = stat["total_orders"] or 0

        # 如果該日期已經有記錄，則更新，否則創建新記錄
        ShopSalesStats.objects.update_or_create(
            shop_id=shop_id,
            date=today,
            defaults={
                "total_sales_amount": total_sales_amount,
                "total_qty": total_qty,
                "total_orders": total_orders,
            },
        )
        print(
            f"Shop {shop_id}: Sales={total_sales_amount}, Qty={total_qty}, Orders={total_orders}"
        )

    base_path = "/Users/rd/Desktop/quiz_12_17/data"

    # 目標資料夾
    folder_path = os.path.join(base_path, f"shop_sales_{today}")

    # 如果資料夾不存在，則創建它
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)

    # 最終的 CSV 檔案路徑
    file_path = os.path.join(folder_path, f"shop_sales_{today}.csv")

    try:
        with open(file_path, mode="w", newline="", encoding="utf-8") as file:
            writer = csv.writer(file)
            writer.writerow(
                [
                    "Shop ID",
                    "Total Sales Amount",
                    "Total Quantity",
                    "Total Orders",
                    "Date",
                ]
            )

            for stat in shop_stats:
                writer.writerow(
                    [
                        stat["shop_id"],
                        stat["total_sales_amount"],
                        stat["total_qty"],
                        stat["total_orders"],
                        yesterday,
                    ]
                )
            print("寫入成功")
    except Exception as e:
        print(f"寫入CSV檔案時發生錯誤: {e}")
