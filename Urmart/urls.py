from Urmart import views
from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns

# urlpatterns = [
#     path('order_create', views.OrderViewSet.as_view({'post': 'order_create'})),
#     path('order_delete', views.OrderViewSet.as_view({'delete': 'order_delete'})),
# path('order_list', views.OrderViewSet.as_view({'get': 'order_list'})),]
# urlpatterns = format_suffix_patterns(urlpatterns)
from rest_framework.routers import DefaultRouter
from .views import OrderViewSet,MemberViewSet,ProductViewSet

# 创建 DefaultRouter 实例
router = DefaultRouter()

router.register(r'orders', OrderViewSet, basename='order')
router.register(r'members', MemberViewSet)
router.register(r'products', ProductViewSet)

urlpatterns = router.urls