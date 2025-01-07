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


class ShopFactory(DjangoModelFactory):
    class Meta:
        model = Shop

    name = factory.Sequence(lambda n: n + 1) #為了要符合 unique=True

class ProductFactory(DjangoModelFactory):
    class Meta:
        model = Product

    stock_pcs = Faker('random_int', min=50, max=200)
    price = Faker('random_number', digits=2)
    shop = factory.SubFactory(ShopFactory)
    is_vip = False


class MemberFactory(DjangoModelFactory):
    class Meta:
        model = Member
        django_get_or_create = ('member_name',)

    member_name = Faker('name')
    is_vip = Faker('boolean')

class OrderFactory(DjangoModelFactory):
    class Meta:
        model = Order
        django_get_or_create = ('order_name',)

    total_price = factory.LazyAttribute(lambda o: sum(item.subtotal for item in o.items.all()))
    member=factory.SubFactory(MemberFactory)


class OrderItemFactory(DjangoModelFactory):
    class Meta:
        model = OrderItem
    order = factory.SubFactory(OrderFactory)
    product = factory.SubFactory(ProductFactory)
    qty=Faker('random_int', min=1, max=100)
    price=Faker('random_number', digits=2)
    subtotal = factory.LazyAttribute(lambda o: o.qty * o.price)



@pytest.fixture
def order():
    shop = Shop.objects.create(name=1)
    member = Member.objects.create(member_name='KK')
    product = Product.objects.create(
        stock_pcs=100, price=Decimal('20'), shop=shop, is_vip=False
    )
    order = Order.objects.create(
        total_price=200,
        member=member,
    )
    orderitem = OrderItem.objects.create(
        order=order,
        product=product,
        qty=100,
        price=Decimal('20'),
        subtotal=Decimal('2000'),
    )
    return order


@pytest.mark.django_db
def test_create_order():
    shop = Shop.objects.create(name=1)
    member = Member.objects.create(member_name='KK')
    product = Product.objects.create(
        stock_pcs=100, price=Decimal('20'), shop_id=shop.id, is_vip=False
    )

    # 建立訂單
    client = APIClient()
    payload = {'member': member.id, 'items': [{'product': product.id, 'qty': 10}]}
    response = client.post(f'/api/orders/', payload, format='json')
    assert response.status_code == status.HTTP_201_CREATED
    order = Order.objects.first()
    product = Product.objects.get(id=product.id)
    assert order is not None
    assert order.total_price == 200
    assert product.stock_pcs == 90, '剩餘庫存錯誤'



@pytest.mark.django_db
def test_order_list():
    client = APIClient()
    response = client.get(f'/api/orders/')
    assert response.status_code == status.HTTP_200_OK

@pytest.mark.django_db
def test_retrieve_order(order):
    client = APIClient()
    response = client.get(f'/api/orders/991/')
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.data['error'] == '該訂單不存在'

@pytest.mark.django_db
def test_partial_update_order(order):
    shop = ShopFactory(name=4)
    member = MemberFactory()
    product = ProductFactory(shop=shop,stock_pcs=100, price=Decimal('20'))
    client = APIClient()
    payload = {'member': member.id, 'items': [{'product': product.id, 'qty': 10}]}
    response = client.post(f'/api/orders/', payload, format='json')
    assert response.status_code == status.HTTP_201_CREATED
    product.refresh_from_db()
    assert product.stock_pcs == 90, '商品庫存未正確減少'

    order_id=response.data['id']
    payload = {'member': member.id, 'items': [{'product': product.id, 'qty': 20}]}
    response = client.patch(f'/api/orders/{order_id}/',payload, format='json')
    assert response.status_code == status.HTTP_200_OK
    product.refresh_from_db()
    assert product.stock_pcs == 80, '商品庫存未正確減少'



# @pytest.mark.django_db
# def test_retrieve_order_detail(order):
#     order=Order.objects.get(id=order.id)
#     client = APIClient()
#     response=client.get(f'/api/orders/{order.id}')
#     assert response

@pytest.mark.django_db
def test_order_delete(order):
    order = Order.objects.first()
    assert order is not None, '找不到訂單編號'
    client = APIClient()
    response = client.delete(f'/api/orders/{order.id}/')
    assert response.status_code == status.HTTP_204_NO_CONTENT, '刪除失敗'

@pytest.mark.django_db
def test_order_delete_adjust_stock(order):
    shop = ShopFactory(name=3)
    product=ProductFactory(stock_pcs=100,shop=shop)
    member=MemberFactory()
    client = APIClient()
    payload = {'member': member.id, 'items': [{'product': product.id, 'qty': 10}]}
    response = client.post(f'/api/orders/', payload, format='json')
    assert response.status_code == status.HTTP_201_CREATED
    product.refresh_from_db()
    assert product.stock_pcs == 90,'商品庫存未正確減少'

    order_id = response.data['id']
    response = client.delete(f'/api/orders/{order_id}/')
    assert response.status_code == status.HTTP_204_NO_CONTENT, '刪除失敗'
    product.refresh_from_db()
    assert product.stock_pcs == 100,'商品庫存未正確恢復'




@pytest.mark.django_db
def test_get_popular_orders():

    shop_1 = ShopFactory()
    shop_2 = ShopFactory()
    shop_3 = ShopFactory()

    product_a = ProductFactory(shop=shop_1)
    product_b = ProductFactory(shop=shop_2)
    product_c = ProductFactory(shop=shop_3)

    member_a = MemberFactory()
    member_b = MemberFactory()
    member_c = MemberFactory()
    member_d = MemberFactory()



    OrderItem.objects.create(
        product=product_a, qty=5, price=product_a.price, order=Order.objects.create(member=member_a)
    )
    OrderItem.objects.create(
        product=product_c, qty=5, price=product_c.price, order=Order.objects.create(member=member_b)
    )
    OrderItem.objects.create(
        product=product_b, qty=30, price=product_b.price, order=Order.objects.create(member=member_c)
    )
    OrderItem.objects.create(
        product=product_a, qty=50, price=product_a.price, order=Order.objects.create(member=member_d)
    )

    client = APIClient()
    response = client.get('/api/orders/top_three_products/')
    assert response.status_code == status.HTTP_200_OK
    data = response.json()

    assert len(data) == 3
    assert data[0]['product_id'] == product_a.id
    assert data[0]['total_sales'] == 55
    assert data[1]['product_id'] == product_b.id
    assert data[1]['total_sales'] == 30
    assert data[2]['product_id'] == product_c.id
    assert data[2]['total_sales'] == 5


#
@pytest.mark.django_db
def test_check_vip_not_allow():
    product_a = ProductFactory(is_vip=True)
    member = MemberFactory(is_vip=False)

    client = APIClient()
    payload = {
        'member': member.id,
        'items': [{'product': product_a.id, 'qty': 1}],

    }
    response = client.post(f'/api/orders/', payload, format='json')

    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.data == {'error': '屬於VIP 商品無法購買'}

@pytest.mark.django_db
def test_check_vip_allow():
    product_a = ProductFactory(is_vip=True)
    member = MemberFactory(is_vip=True)

    client = APIClient()
    payload = {
        'member': member.id,
        'items': [{'product': product_a.id, 'qty': 1}],

    }
    response = client.post(f'/api/orders/', payload, format='json')

    assert response.status_code == status.HTTP_201_CREATED


@pytest.mark.django_db
def test_check_vip_allow():
    product_a = ProductFactory(is_vip=True)
    member = MemberFactory(is_vip=True)

    client = APIClient()
    payload = {
        'member': member.id,
        'items': [{'product': product_a.id, 'qty': 1}],

    }
    response = client.post(f'/api/orders/', payload, format='json')

    assert response.status_code == status.HTTP_201_CREATED

@pytest.mark.django_db
def test_check_stock_not_allow():
    product_a = ProductFactory(stock_pcs=20)
    member = MemberFactory()
    client = APIClient()
    payload = {'member': member.id, 'items': [{'product': product_a.id, 'qty': 100}]}

    response = client.post(f'/api/orders/', payload, format='json')
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert f'僅剩{product_a.stock_pcs} 件可用'

@pytest.mark.django_db
def test_check_stock_allow():
    product_a = ProductFactory(stock_pcs=20)
    member = MemberFactory()
    client = APIClient()
    payload = {'member': member.id, 'items': [{'product': product_a.id, 'qty': 5}]}

    response = client.post(f'/api/orders/', payload, format='json')
    assert response.status_code == status.HTTP_201_CREATED

