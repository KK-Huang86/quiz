from django.db import transaction
from rest_framework import serializers

from urmart.models import Member, Order, OrderItem, Product, Shop


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = "__all__"


class ShopSerializer(serializers.ModelSerializer):
    class Meta:
        model = Shop
        fields = "__all__"


class MemberSerializer(serializers.ModelSerializer):
    class Meta:
        model = Member
        fields = "__all__"


class OrderItemSerializer(serializers.ModelSerializer):
    product=serializers.PrimaryKeyRelatedField(queryset=Product.objects.all())

    class Meta:
        model = OrderItem
        fields = ["product", "qty", "price", "subtotal"]
        read_only_fields = ["price", "subtotal"]

    def validate(self, data):
        product=data.get("product")
        qty=data.get("qty")

        if product and product.stock_pcs < qty:
            raise serializers.ValidationError(f'{product.name} 商品庫存不足，僅剩{product.stock_pcs} 件可用')
        return data

    def create(self, validated_data):
        # product = validated_data.get('product')
        # qty = validated_data.get('qty')
        #
        # # 在創建訂單項目時更新庫存
        # product.adjust_stock(-qty)  # 減少庫存
        return super().create(validated_data)
        # return order_item

class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True, write_only=True)
    member = serializers.PrimaryKeyRelatedField(queryset=Member.objects.all())
    total_price = serializers.DecimalField(
        max_digits=10, decimal_places=0, read_only=True
    )
    order_items = OrderItemSerializer(source='orderitem_set', many=True, read_only=True)

    class Meta:
        model = Order
        fields = [
            "id",
            "member",
            "total_price",
            "items",
            "order_items"
        ]

    def create(self, validated_data):
        items_data = validated_data.pop('items')  # 取出訂單項目
        member = validated_data.pop('member')
        print(f'-----{member}{items_data}-----')
        order = Order.objects.create(member=member,**validated_data)  # 創建訂單
        print(validated_data)

        for item_data in items_data:
            # 為每個訂單項目創建 OrderItem
            OrderItem.objects.create(order=order, **item_data)

        order.calculate_total_price()  # 計算總金額
        return order

    def validate_member(self, value):
        """驗證會員是否存在且有效"""
        if not value:
            raise serializers.ValidationError("請輸入有效的會員")
        return value

