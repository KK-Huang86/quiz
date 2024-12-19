from functools import wraps
from django.http import HttpResponse

from Urmart.models import Product


def check_vip_identity(view_func):
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        product_id = request.request.get("product_id")
        print(f'============================request {request}, product_id {product_id}')
        try:
            product=Product.objects.get(id=product_id)
            print({product})
        except Product.DoesNotExist:
            return HttpResponse("商品不存在",status=404)
        if not product.is_vip:
            return  HttpResponse("商品不符合VIP資格",status=403)
        return view_func(request, *args, **kwargs)
    return wrapper

def check_stock(view_func):
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        product_id = request.data.get('product_id')
        qty=request.data.get('qty')
        try:
            product = Product.objects.get(id=product_id)
        except Product.DoesNotExist:
            return HttpResponse("商品不存在",status=404)

        if product.stock_pcs < qty:
            return HttpResponse("商品庫存不夠，無法購買",status=404)
        return view_func(request, *args, **kwargs)
    return wrapper

