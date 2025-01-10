from functools import wraps

from rest_framework import status
from rest_framework.request import Request
from rest_framework.response import Response

from urmart.models import Member, Product

def check_vip_identity(view_func):
    @wraps(view_func)
    def wrapper(view_instance, request, *args, **kwargs):
        if not isinstance(request, Request):
            return Response(
                {'error': '無效的請求'}, status=status.HTTP_400_BAD_REQUEST
            )  # 確保 request是否為DRF中Request類型

        # 從viewset傳入 request.data
        data = request.data
        print(f'Request Data: {request.data}')

        # 獲取 member_id，檢查是否存在
        member_id = data.get('member')
        if not member_id:
            return Response(
                {'error': '會員資訊缺失'}, status=status.HTTP_400_BAD_REQUEST
            )

        try:
            member = Member.objects.get(id=member_id)  # 確認會員是否存在
        except Member.DoesNotExist:
            return Response({'error': '會員不存在'}, status=status.HTTP_404_NOT_FOUND)

        # 遍歷 items 中的每個商品進行檢查
        items = data.get('items', '')
        if not items:
            return Response(
                {'error': '訂單項目缺失'}, status=status.HTTP_400_BAD_REQUEST
            )

        for item in items:
            product_id = item.get('product')
            if not product_id:
                return Response(
                    {'error': '商品資訊缺失'}, status=status.HTTP_400_BAD_REQUEST
                )

            try:
                product = Product.objects.get(id=product_id)  # 確認商品是否存在
            except Product.DoesNotExist:
                return Response(
                    {'error': '商品不存在'}, status=status.HTTP_404_NOT_FOUND
                )

            # 檢查是否是 VIP 商品，並且會員是否為 VIP
            if product.is_vip and not member.is_vip:
                return Response(
                    {'error': f'{product.name}屬於VIP 商品無法購買'},
                    status=status.HTTP_400_BAD_REQUEST,
                )

        return view_func(view_instance, request, *args, **kwargs)

    return wrapper
