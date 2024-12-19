from rest_framework import serializers
from Urmart.models import Product,Order,Member
from django.db import transaction


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model=Product
        fields='__all__'

class MemberSerializer(serializers.ModelSerializer):
    class Meta:
        model=Member
        fields='__all__'

class OrderSerializer(serializers.ModelSerializer):
    product = serializers.PrimaryKeyRelatedField(queryset=Product.objects.all())
    member_id = serializers.PrimaryKeyRelatedField(queryset=Member.objects.all())
    class Meta:
        model=Order
        fields = ['id', 'product', 'qty', 'price', 'shop_id', 'member_id']

    def update_product_stock(self, product,qty,action):
        with transaction.atomic(): #原子操作
            if action=='remove':
                if product.stock_pcs < qty:
                    raise serializers.ValidationError("商品庫存不足")
                product.stock_pcs -= qty
            elif action =="add":
                product.stock_pcs += qty
            product.save()

    def create(self, validated_data):
            product = validated_data['product']
            qty = validated_data['qty']
            member = validated_data['member_id']
            if product.stock_pcs <=0:
                raise serializers.ValidationError("目前庫存不足")
            # 在創建訂單時，減少商品庫存
            self.update_product_stock(product, qty, action='remove')  # 減少庫存
            validated_data['member_id'] = member.id
            return Order.objects.create(**validated_data)
