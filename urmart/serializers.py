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
    class Meta:
        model = OrderItem
        fields = ["product", "qty", "price", "subtotal"]


class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True, write_only=True)
    member_id = serializers.PrimaryKeyRelatedField(queryset=Member.objects.all())
    total_price = serializers.DecimalField(
        max_digits=10, decimal_places=0, read_only=True
    )

    class Meta:
        model = Order
        fields = [
            "id",
            "member_id",
            "total_price",
            "items",
        ]

    def validate(self, attrs):
        # 驗證商品庫存
        items = attrs.get("items", [])
        for item in items:
            product = item.get("product")
            qty = item.get("qty")
            if product.stock_pcs < qty:
                raise serializers.ValidationError(f"商品 {product.name} 的庫存不足")
        return attrs

    def create(self, validated_data):
        items_data = validated_data.pop("items")
        print(validated_data)

        # 獲取 member 實例
        member = validated_data.pop(
            "member_id"
        )  # 這裡可以直接使用 `member_id`，它已經是 `Member` 實例
        print(member)
        member_id = member.id
        print(member_id)

        # 創建訂單
        order = Order.objects.create(member_id=member_id, **validated_data)

        total_price = 0
        with transaction.atomic():  # 保證原子操作
            for item_data in items_data:
                product = item_data["product"]
                qty = item_data["qty"]
                price = item_data["price"]

                # 減少商品庫存
                if product.stock_pcs < qty:
                    raise serializers.ValidationError(
                        f"商品 {product.name} 庫存不足，無法訂購此數量"
                    )
                product.stock_pcs -= qty
                product.save()

                # 創建訂單項目
                order_item = OrderItem.objects.create(
                    order=order, product=product, qty=qty, price=price
                )
                total_price += order_item.subtotal  # 使用 `subtotal` 自動計算小計

        # 更新訂單的總金額
        order.total_price = total_price
        order.save()

        return order
