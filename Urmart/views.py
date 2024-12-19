from pickle import FALSE

from .models import Order,Product,Member
from .serializers import ProductSerializer,OrderSerializer,MemberSerializer
from .decorators import check_vip_identity, check_stock
from rest_framework import viewsets, mixins
from rest_framework.decorators import action
from rest_framework import status
from rest_framework.response import Response
from django.db.models import Sum


class MemberViewSet(viewsets.ModelViewSet):
    queryset = Member.objects.all()
    serializer_class = MemberSerializer

class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

class OrderViewSet(mixins.CreateModelMixin,mixins.DestroyModelMixin,mixins.ListModelMixin,viewsets.GenericViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer

    @action(detail=False, methods=['post'])
    # @check_vip_identity
    # @check_stock
    def order_create(self, request):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save() #觸發 create
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['delete'])
    # @check_stock
    def order_delete(self,request,pk):
        try:
            order = Order.objects.get(id=pk)
            self.serializer_class().update_product_stock(order.product, order.qty, action='add')
            order.product.save()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Order.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

    @action(detail=False, methods=['get'])
    def top_three_product(self):
        top_products=(Order.objects.values('product__id').annotate(total_sales=Sum('qty')).order_by('-total_sales')[:3])

        data = [
         {
            'product_id': product['product__id'],
            'total_sales': product['total_sales'],
            }
            for product in top_products
        ]

        return Response(data, status=status.HTTP_200_OK)

    @action(detail=False, methods=['get'])
    def order_list(self,request):
        orders = Order.objects.all()
        serializer = self.get_serializer(orders, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

