import json
from functools import wraps

from django.http import HttpResponse

from Urmart.models import Product


def check_vip_identity(view_func):
    @wraps(view_func)
    def wrapper(*args, **kwargs):
        request = kwargs.get("request")
        print(request)
        for arg in args:
            print(arg)
        print("args", args)
        print("kwargs", kwargs)

        # request_data = {
        #     'method': request.method,
        #     'path': request.path,
        #     'GET': request.GET.dict(),
        #     'POST': request.POST.dict(),
        #     'headers': dict(request.headers),
        # }
        # print(json.dumps(request_data, indent=4))
        print(f"dir(request): {dir(request)}")

        # print(f'request: {request}, {request.__dict__}')
        # product_id = kwargs.get("product_id")
        # print(product_id)
        # try:
        #     product = Product.objects.get(product_id=product_id)
        #     print({product})
        # except Product.DoesNotExist:
        #     return HttpResponse("商品不存在", status=404)
        # if product.is_vip:
        #     return HttpResponse("商品符合VIP資格，您無法購買", status=403)
        return view_func(*args, **kwargs)

    return wrapper


# def check_stock(view_func):
#     @wraps(view_func)
#     def wrapper(request, *args, **kwargs):
#         product_id = request.data.get("product_id")
#         qty = request.data.get("qty")
#         try:
#             product = Product.objects.get(id=product_id)
#         except Product.DoesNotExist:
#             return HttpResponse("商品不存在", status=404)
#
#         if product.stock_pcs < qty:
#             return HttpResponse("商品庫存不夠，無法購買", status=404)
#         return view_func(request, *args, **kwargs)
#
#     return wrapper
