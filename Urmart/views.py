import datetime
import os
from pickle import FALSE

import pytz
import requests
from celery import Celery
from django.db import transaction
from django.db.models import Sum
from rest_framework import (mixins, permissions, serializers, status, views,
                            viewsets)
from rest_framework.decorators import action
from rest_framework.response import Response

from .decorators import check_vip_identity
from .models import Member, Order, Product
from .serializers import MemberSerializer, OrderSerializer, ProductSerializer
from .task import test_task
from celery import shared_task


class MemberViewSet(viewsets.ModelViewSet):
    queryset = Member.objects.all()
    serializer_class = MemberSerializer


class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer


class OrderViewSet(
    mixins.CreateModelMixin,
    mixins.DestroyModelMixin,
    mixins.ListModelMixin,
    viewsets.GenericViewSet,
):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer

    @check_vip_identity
    # @check_stock
    def create(self, request, pk=None):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            validated_data = serializer.validated_data #取出 serializer 過的資料
            product = validated_data["product"]
            qty = validated_data["qty"]
            price = validated_data["price"]
            member = validated_data["member_id"]
            total_price = qty * price
            # 庫存檢查
            if product.stock_pcs <= 0:
                return Response(
                    {"error": "目前庫存不足"}, status=status.HTTP_400_BAD_REQUEST
                )
            if product.stock_pcs < qty:
                return Response(
                    {"error": "庫存不足，無法下單"}, status=status.HTTP_400_BAD_REQUEST
                )
            # 減少商品庫存
            with transaction.atomic():  # 保證原子操作
                product.stock_pcs -= qty
                product.save()

            # 計算訂單價格
            validated_data["total_price"] = total_price
            # 設定會員ID
            validated_data["member_id"] = member.id

            # 創建訂單
            order = Order.objects.create(**validated_data)
            return Response(OrderSerializer(order).data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def retrieve(self, request, pk=None):
        try:
            order = Order.objects.get(pk=pk)
            return Response(OrderSerializer(order).data, status=status.HTTP_200_OK)

        except Order.DoesNotExist:
            return Response({"error":"該訂單不存在"},status=status.HTTP_404_NOT_FOUND)


    #@check_stock
    def destroy(self, request, pk):
        try:
            order = Order.objects.get(id=pk)
            product = order.product
            qty = order.qty
            product.stock_pcs += qty
            product.save()
            order.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Order.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

    @action(detail=False, methods=["get"])
    def top_three_products(self, request):
        top_products = (
            Order.objects.values("product__id")
            .annotate(total_sales=Sum("qty"))
            .order_by("-total_sales")[:3]
        )

        data = [
            {
                "product_id": product["product__id"],
                "total_sales": product["total_sales"],
            }
            for product in top_products
        ]

        return Response(data, status=status.HTTP_200_OK)


# celery 異步任務

class test_async_task(views.APIView):
    permission_classes = (permissions.AllowAny,)
    authentication_classes = []

    def post(self, request):
        id = request.data.get("id")

        os.environ.setdefault("DJANGO_SETTINGS_MODULE", "core.settings")
        app = Celery("core")
        app.config_from_object("django.conf:settings", namespace="CELERY")
        app.autodiscover_tasks()

        local_timezone = pytz.timezone("Asia/Taipei")
        now = datetime.datetime.now()
        # 60秒後執行
        exec_time = now + datetime.timedelta(seconds=90)
        # 利用 pytz 進行轉換
        exec_time = local_timezone.localize(exec_time)

        # apply_async 異步執行，多進程安排執行任務，eta時間差，這邊是60秒後執行
        test_task.apply_async(args=(id,), eta=exec_time)

        return Response(
            {"success": True, "message": "執行成功"}, status=status.HTTP_200_OK
        )
#
# @shared_task()
# def test_task(id):
#     user_email="hsinkai@urmart.com"