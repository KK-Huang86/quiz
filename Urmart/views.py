

from .models import Order,Product
from .serializers import ProductSerializer,OrderSerializer
from .decorators import check_vip_identity, check_stock
from rest_framework import viewsets, mixins
from rest_framework.decorators import action
from rest_framework import status
from rest_framework.response import Response


class OrderViewSet(mixins.CreateModelMixin,mixins.DestroyModelMixin,viewsets.GenericViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer

    @action(detail=False, methods=['post'])
    @check_vip_identity
    @check_stock
    def order_create(self, request):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['delete'])
    @check_stock
    def order_delete(self,request,pk):
        try:
            order = Order.objects.get(id=pk)
            order.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Order.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

