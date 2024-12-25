from django.utils import timezone

from rest_framework.test import APIClient
from Urmart.models import Member,Product,Order
from rest_framework import status
import pytest


@pytest.fixture
def order():
    member = Member.objects.create(member_name="KK")
    product = Product.objects.create(stock_pcs=100, price="20", shop_id=2, is_vip=False)
    order = Order.objects.create(
        product=product,
        qty=10,
        price=product.price,
        shop_id=product.shop_id,
        member_id=member.id,
        # create_time=timezone.now(), #自動生成，不需要手動輸入
    )
    return order

@pytest.mark.django_db
def test_create_order():
    member = Member.objects.create(member_name="KK")
    product = Product.objects.create(stock_pcs=100,price="20",shop_id=2,is_vip=False)

    #建立訂單
    client = APIClient()
    payload ={
        'product':product.id,
        'qty':10,
        'price':product.price,
        'shop_id':product.shop_id,
        'member_id':member.id,
        'create_time':timezone.now(),
    }
    response = client.post(f"/api/orders/", payload, format="json")
    assert response.status_code == status.HTTP_201_CREATED
    order = Order.objects.first()
    product=Product.objects.get(id=product.id)
    assert order is not None
    assert order.total_price== 200
    assert product.stock_pcs == 90,"剩餘庫存錯誤"

@pytest.mark.django_db
def test_order_list():
    client = APIClient()
    response = client.get(f"/api/orders/")
    assert response.status_code == status.HTTP_200_OK


@pytest.mark.django_db
def test_order_delete(order):
    order = Order.objects.first()
    assert order is not None,"找不到訂單編號"
    client = APIClient()
    response = client.delete(f"/api/orders/{order.id}/")
    assert response.status_code == status.HTTP_204_NO_CONTENT,"刪除失敗"

@pytest.mark.django_db
def test_get_popular_orders():
    order = Order.objects.values("")[:3]
    client = APIClient()
