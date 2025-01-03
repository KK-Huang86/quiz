import json
from decimal import Decimal
from itertools import product

import factory
import pytest
from django.db.models import Sum
from django.utils import timezone
from factory import Faker
from factory.django import DjangoModelFactory
from rest_framework import status
from rest_framework.test import APIClient

from urmart.decorators import check_vip_identity
from urmart.models import Member, Order, OrderItem, Product, Shop
from urmart.views import OrderViewSet


class ProductFactory(DjangoModelFactory):
    class Meta:
        model = Product

    stock_pcs = Faker("random_int", min=50, max=200)
    price = Faker("random_number", digits=2)
    shop_id = 2
    is_vip = False


class MemberFactory(DjangoModelFactory):
    class Meta:
        model = Member
        django_get_or_create = ("member_name",)

    member_name = Faker("name")
    is_vip = Faker("boolean")

class OrderItemFactory(DjangoModelFactory):
    class Meta:
        model = OrderItem


@pytest.fixture
def order():
    shop = Shop.objects.create(name=1)
    member = Member.objects.create(member_name="KK")
    product = Product.objects.create(
        stock_pcs=100, price=Decimal("20"), shop=shop, is_vip=False
    )
    order = Order.objects.create(
        total_price=200,
        member=member,
    )
    orderitem = OrderItem.objects.create(
        order=order,
        product=product,
        qty=100,
        price=Decimal("20"),
        subtotal=Decimal("2000"),
    )
    return order


@pytest.mark.django_db
def test_create_order():
    shop = Shop.objects.create(name=1)
    member = Member.objects.create(member_name="KK")
    product = Product.objects.create(
        stock_pcs=100, price=Decimal("20"), shop_id=shop.id, is_vip=False
    )

    # 建立訂單
    client = APIClient()
    payload = {"member": member.id, "items": [{"product": product.id, "qty": 10}]}
    response = client.post(f"/api/orders/", payload, format="json")
    assert response.status_code == status.HTTP_201_CREATED
    order = Order.objects.first()
    product = Product.objects.get(id=product.id)
    assert order is not None
    assert order.total_price == 200
    assert product.stock_pcs == 90, "剩餘庫存錯誤"



@pytest.mark.django_db
def test_order_list():
    client = APIClient()
    response = client.get(f"/api/orders/")
    assert response.status_code == status.HTTP_200_OK

@pytest.mark.django_db
def test_retrieve_order(order):
    client = APIClient()
    response = client.get(f"/api/orders/991/")
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.data["error"] == "該訂單不存在"


# @pytest.mark.django_db
# def test_retrieve_order_detail(order):
#     order=Order.objects.get(id=order.id)
#     client = APIClient()
#     response=client.get(f'/api/orders/{order.id}')
#     assert response

@pytest.mark.django_db
def test_order_delete(order):
    order = Order.objects.first()
    assert order is not None, "找不到訂單編號"
    client = APIClient()
    response = client.delete(f"/api/orders/{order.id}/")
    assert response.status_code == status.HTTP_204_NO_CONTENT, "刪除失敗"
#
#
@pytest.mark.django_db
def test_get_popular_orders():
#     product_a = Product.objects.create(
#         stock_pcs=100, price="20", shop_id=2, is_vip=False
#     )
#     product_b = Product.objects.create(
#         stock_pcs=120, price="10", shop_id=1, is_vip=False
#     )
#     product_c = Product.objects.create(
#         stock_pcs=150, price="50", shop_id=2, is_vip=False
#     )

    product_a=ProductFactory()
    product_b=ProductFactory()
    product_c=ProductFactory()

    member_a = MemberFactory()
    member_b = MemberFactory()
    member_c = MemberFactory()
    member_d = MemberFactory()
#
    Order.objects.create(
        product=product_a,
        qty=5,
        price=product_a.price,
        shop_id=2,
        member_id=member_a.id,
    )
    Order.objects.create(
        product=product_c,
        qty=5,
        price=product_c.price,
        shop_id=1,
        member_id=member_b.id,
    )
    Order.objects.create(
        product=product_b,
        qty=30,
        price=product_b.price,
        shop_id=1,
        member_id=member_c.id,
    )
    Order.objects.create(
        product=product_a,
        qty=50,
        price=product_a.price,
        shop_id=3,
        member_id=member_d.id,
    )

    top_products = (
        Order.objects.values("product__id")
        .annotate(total_sales_qty=Sum("qty"))
        .order_by("-total_sales_qty")[:3]
    )
#
    assert len(top_products) == 3, "只抓三個"
    assert top_products[0]["product__id"] == product_a.id
    assert top_products[1]["product__id"] == product_b.id
    assert top_products[2]["product__id"] == product_c.id

    assert top_products[0]["total_sales_qty"] == 55
    assert top_products[1]["total_sales_qty"] == 30
    assert top_products[2]["total_sales_qty"] == 5
#
#
# @pytest.mark.django_db
# def test_check_vip_not_allow():
#     product_a = Product.objects.create(
#         stock_pcs=100, price="20", shop_id=2, is_vip=True
#     )
#     member = MemberFactory()
#
#     client = APIClient()
#     payload = {
#         "product": product_a.id,
#         "qty": 10,
#         "price": product_a.price,
#         "shop_id": product_a.shop_id,
#         "member_id": member.id,
#     }
#     response = client.post(f"/api/orders/", payload, format="json")
#
#     assert response.status_code == status.HTTP_400_BAD_REQUEST
#     assert response.data == {"error": "VIP 商品無法購買"}
#
#
# @pytest.mark.django_db
# def test_check_vip_allow():
#     product_b = Product.objects.create(
#         stock_pcs=100, price="10", shop_id=1, is_vip=False
#     )
#     member = MemberFactory()
#     client = APIClient()
#     payload = {
#         "product": product_b.id,
#         "qty": 10,
#         "price": product_b.price,
#         "shop_id": product_b.shop_id,
#         "member_id": member.id,
#     }
#     response = client.post(f"/api/orders/", payload, format="json")
#     assert response.status_code == status.HTTP_201_CREATED
#
#
# @pytest.mark.django_db
# def test_check_stock_allow():
#     product_c = Product.objects.create(
#         stock_pcs=30, price="10", shop_id=1, is_vip=False
#     )
#     member = MemberFactory()
#     client = APIClient()
#     payload = {
#         "product": product_c.id,
#         "qty": 10,
#         "price": product_c.price,
#         "shop_id": product_c.shop_id,
#         "member_id": member.id,
#     }
#     response = client.post(f"/api/orders/", payload, format="json")
#     assert response.status_code == status.HTTP_201_CREATED
#
#
# @pytest.mark.django_db
# def test_check_stock_not_allow():
#     product_d = Product.objects.create(stock_pcs=5, price="10", shop_id=1, is_vip=False)
#     member = MemberFactory()
#     client = APIClient()
#     payload = {
#         "product": product_d.id,
#         "qty": 10,
#         "price": product_d.price,
#         "shop_id": product_d.shop_id,
#         "member_id": member.id,
#     }
#     response = client.post(f"/api/orders/", payload, format="json")
#     print(response.data)
#     assert response.status_code == status.HTTP_400_BAD_REQUEST
