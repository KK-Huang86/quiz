import datetime
import os

import pytz
from celery import Celery
from django.db import transaction
from django.db.models import Sum
from rest_framework import mixins, permissions, status, views, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from .decorators import check_stock, check_vip_identity
from .models import Member, Order, OrderItem, Product, Shop
from .serializers import (MemberSerializer, OrderItemSerializer,
                          OrderSerializer, ProductSerializer, ShopSerializer)
from .task import test_task


class MemberViewSet(viewsets.ModelViewSet):
    queryset = Member.objects.all()
    serializer_class = MemberSerializer


class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer


class ShopViewSet(viewsets.ModelViewSet):
    queryset = Shop.objects.all()
    serializer_class = ShopSerializer


class OrderItemViewSet(viewsets.ModelViewSet):
    queryset = OrderItem.objects.all()
    serializer_class = OrderItemSerializer


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
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        order = serializer.save()  # 呼叫 serializer 的 create 方法
        return Response(self.get_serializer(order).data, status=status.HTTP_201_CREATED)

    def retrieve(self, request, pk=None):
        try:
            order = Order.objects.get(pk=pk)
            order_serializer = OrderSerializer(order)
            return Response(order_serializer.data, status=status.HTTP_200_OK)

        except Order.DoesNotExist:
            return Response({"error": "該訂單不存在"}, status=status.HTTP_404_NOT_FOUND)

    @check_stock
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
            Order.objects.values("product__id")  # 抓取每一個 Order 內的 product id
            .annotate(total_sales=Sum("qty"))  # 計算每個 product 的總銷售數量
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

    def post(self, request, *args, **kwargs):
        id = request.data.get("id")

        os.environ.setdefault("DJANGO_SETTINGS_MODULE", "core.settings")
        app = Celery("core")
        app.config_from_object("django.conf:settings", namespace="CELERY")
        app.autodiscover_tasks()

        local_timezone = pytz.timezone("Asia/Taipei")
        now = datetime.datetime.now()
        # 90秒後執行
        exec_time = now + datetime.timedelta(seconds=90)
        # 利用 pytz 進行轉換
        exec_time = local_timezone.localize(exec_time)

        # apply_async 異步執行，多進程安排執行任務，eta時間差，這邊是60秒後執行
        test_task.apply_async(args=(id,), eta=exec_time)

        return Response(
            {"success": True, "message": "執行成功"}, status=status.HTTP_200_OK
        )
