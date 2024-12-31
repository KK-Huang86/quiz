from functools import wraps

from rest_framework import status
from rest_framework.request import Request
from rest_framework.response import Response

from urmart.models import Member, Product

# def check_vip_identity(view_func):
#     @wraps(view_func)
#     def wrapper(*args, **kwargs):
#         view_instance = args[0]  #
#         request = args[1]  # 取得request物件
#         validated_data = request.data
#         product_id = validated_data.get('product')
#
#         # 如果有商品ID，檢查是否為VIP商品
#         if product_id:
#             try:
#                 product = Product.objects.get(id=product_id)
#
#                 # 如果商品是VIP商品，返回錯誤
#                 if product.is_vip:
#                     return Response(
#                         {"error": "此商品僅限VIP會員購買，不能購買此商品"},
#                         status=status.HTTP_400_BAD_REQUEST
#                     )
#             except Product.DoesNotExist:
#                 return Response(
#                     {"error": "商品不存在"},
#                     status=status.HTTP_400_BAD_REQUEST
#                 )
#         else:
#             return Response(
#                 {"error": "無法獲取商品資料"},
#                 status=status.HTTP_400_BAD_REQUEST
#             )
#
#         # 進行視圖函數的處理
#         return view_func(*args, **kwargs)
#
#     return wrapper
#
#
#
# def check_stock(view_func):
#     @wraps(view_func)
#     def wrapper(*args, **kwargs):
#         view_instance = args[0]
#         request = args[1]
#         validated_data = request.data
#         product_id = validated_data.get('product')
#         qty = request.data.get("qty")
#         if not product_id or qty is None:
#             return Response({"error": "缺少商品或數量資訊"}, status=status.HTTP_400_BAD_REQUEST)
#         try:
#             qty = int(qty)
#             product = Product.objects.get(id=product_id)
#         except Product.DoesNotExist:
#             return Response("商品不存在", status=404)
#
#         if product.stock_pcs < qty:
#             return Response("商品庫存不夠，無法購買", status=404)
#         return view_func(request, *args, **kwargs)
#
#     return wrapper


def check_vip_identity(view_func):
    @wraps(view_func)
    def wrapper(view_instance, request, *args, **kwargs):
        if not isinstance(request, Request):
            return Response(
                {"error": "無效的請求"}, status=status.HTTP_400_BAD_REQUEST
            )  # 確保 request是否為DRF中Request類型

        # serializer = view_instance.get_serializer(data=request.data)
        # serializer.is_valid(raise_exception=True)
        # validated_data = serializer.validated_data

        data = request.data
        print(f"Request Data: {request.data}")

        # 獲取 member_id，檢查是否存在
        member_id = data.get("member")
        if not member_id:
            return Response(
                {"error": "會員資訊缺失"}, status=status.HTTP_400_BAD_REQUEST
            )

        try:
            member = Member.objects.get(id=member_id)  # 確認會員是否存在
        except Member.DoesNotExist:
            return Response({"error": "會員不存在"}, status=status.HTTP_404_NOT_FOUND)

        # 遍歷 items 中的每個商品進行檢查
        items = data.get("items", [])
        if not items:
            return Response(
                {"error": "訂單項目缺失"}, status=status.HTTP_400_BAD_REQUEST
            )

        for item in items:
            product_id = item.get("product")
            if not product_id:
                return Response(
                    {"error": "商品資訊缺失"}, status=status.HTTP_400_BAD_REQUEST
                )

            try:
                product = Product.objects.get(id=product_id)  # 確認商品是否存在
            except Product.DoesNotExist:
                return Response(
                    {"error": "商品不存在"}, status=status.HTTP_404_NOT_FOUND
                )

            # 檢查是否是 VIP 商品，並且會員是否為 VIP
            if product.is_vip and not member.is_vip:
                return Response(
                    {"error": f'{product.name}屬於VIP 商品無法購買'}, status=status.HTTP_400_BAD_REQUEST
                )

        # 如果所有檢查都通過，執行原始的視圖處理
        return view_func(view_instance, request, *args, **kwargs)

    return wrapper


# def check_stock(view_func):
#     @wraps(view_func)
#     def wrapper(view_instance, request, *args, **kwargs):
#         if not isinstance(request, Request):
#             return Response({"error": "無效的請求"}, status=400)
#
#         data = request.data
#         product_id = data.get("product")
#         qty = data.get("qty")
#
#         if view_instance.action == "destroy":
#             return view_func(view_instance, request, *args, **kwargs)
#
#         if not product_id or qty is None:
#             return Response(
#                 {"error": "缺少商品或數量資訊"}, status=status.HTTP_400_BAD_REQUEST
#             )
#         try:
#             qty = int(qty)
#             product = Product.objects.get(id=product_id)
#         except Product.DoesNotExist:
#             return Response("商品不存在", status=404)
#
#         if product.stock_pcs < qty:
#             return Response("商品庫存不夠，無法購買", status=400)
#         return view_func(view_instance, request, *args, **kwargs)
#
#     return wrapper


# def check_stock(view_func):
#     @wraps(view_func)
#     def wrapper(view_instance, request, *args, **kwargs):
#         if not isinstance(request, Request):
#             return Response({"error": "無效的請求"}, status=status.HTTP_400_BAD_REQUEST)
#
#         data = request.data
#         product_id = data.get('product')
#         qty = data.get('qty')
#
#         if not product_id or qty is None:
#             return Response({"error": "缺少商品或數量資訊"}, status=status.HTTP_400_BAD_REQUEST)
#
#         try:
#             qty = int(qty)
#             product = Product.objects.get(id=product_id)
#         except Product.DoesNotExist:
#             return Response({"error": "商品不存在"}, status=status.HTTP_404_NOT_FOUND)
#
#         if product.stock_pcs < qty:
#             return Response(
#                 {"error": "商品庫存不夠，無法購買"},
#                 status=status.HTTP_400_BAD_REQUEST,
#             )
#
#         return view_func(view_instance, request, *args, **kwargs)
#
#     return wrapper
