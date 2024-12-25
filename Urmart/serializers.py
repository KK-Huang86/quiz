from django.db import transaction
from rest_framework import serializers

from Urmart.models import Member, Order, Product


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = "__all__"


class MemberSerializer(serializers.ModelSerializer):
    class Meta:
        model = Member
        fields = "__all__"


class OrderSerializer(serializers.ModelSerializer):
    product = serializers.PrimaryKeyRelatedField(queryset=Product.objects.all())
    member_id = serializers.PrimaryKeyRelatedField(queryset=Member.objects.all())
    total_price = serializers.DecimalField(
        max_digits=10, decimal_places=0, read_only=True
    )

    class Meta:
        model = Order
        fields = [
            "id",
            "product",
            "qty",
            "price",
            "shop_id",
            "member_id",
            "total_price",
        ]

