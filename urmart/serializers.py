from django.db import transaction
from rest_framework import serializers

from urmart.models import Member, Order, OrderItem, Product, Shop


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'


class ShopSerializer(serializers.ModelSerializer):
    class Meta:
        model = Shop
        fields = '__all__'


class MemberSerializer(serializers.ModelSerializer):
    class Meta:
        model = Member
        fields = '__all__'


class OrderItemSerializer(serializers.ModelSerializer):
    product = serializers.PrimaryKeyRelatedField(queryset=Product.objects.all())
    subtotal=serializers.SerializerMethodField()

    class Meta:
        model = OrderItem
        fields = ['id', 'product', 'qty', 'price', 'subtotal']
        read_only_fields = ['price', 'subtotal']

    def validate(self, data):
        product = data.get('product')
        qty = data.get('qty')

        if product and product.stock_pcs < qty:
            raise serializers.ValidationError(
                f'商品編號：{product.id} 商品名稱：{product.name} 商品庫存不足，僅剩{product.stock_pcs} 件可用'
            )
        return data

    def create(self, validated_data):

        return super().create(validated_data)

    def get_subtotal(self, obj):
        return obj.subtotal

class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True, write_only=True)
    member = serializers.PrimaryKeyRelatedField(queryset=Member.objects.all())
    total_price = serializers.DecimalField(
        max_digits=10, decimal_places=0, read_only=True
    )
    order_items = OrderItemSerializer(source='items', many=True, read_only=True)

    class Meta:
        model = Order
        fields = ['id', 'member', 'total_price', 'items', 'order_items']

    def create(self, validated_data):
        items_data = validated_data.pop('items',None)  # 取出訂單項目
        # member = validated_data.pop('member')
        # print(f'-----{items_data}-----')
        order = Order.objects.create(**validated_data)  # 創建訂單
        print(f"-------'validated_data'{validated_data}")

        for item_data in items_data:
            # 為每個訂單項目創建 OrderItem
            OrderItem.objects.create(order=order, **item_data)

        order.calculate_total_price()  # 計算總金額
        return order

    def update(self, instance, validated_data):
        items_data = validated_data.pop('items',None)
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()

        if items_data:
            for item in instance.items.all():
                item.product.stock_pcs += item.qty
                item.product.save()
                item.delete()

            for item_data in items_data:
                product = Product.objects.get(id=item_data['product'].id)
                if product.stock_pcs < item_data['qty']:
                    raise serializers.ValidationError(
                        f'{product.name} 庫存不足，僅剩 {product.stock_pcs} 件可用'
                    )
                product.stock_pcs -= item_data['qty']  # 減少新訂單的庫存
                product.save()
            for item_data in items_data:
                OrderItem.objects.create(order=instance, **item_data)

        instance.calculate_total_price()
        return instance
