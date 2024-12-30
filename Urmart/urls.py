from django.urls import include, path
from django.views.decorators.csrf import csrf_exempt
from rest_framework.routers import DefaultRouter

from .views import MemberViewSet, OrderViewSet, ProductViewSet, test_async_task,ShopViewSet

router = DefaultRouter()

router.register(r'orders', OrderViewSet, basename='order')
router.register(r'members', MemberViewSet)
router.register(r'products', ProductViewSet)
router.register(r'shop',ShopViewSet)

urlpatterns = [
    path("api/", include(router.urls)),
    path("api/test_task", csrf_exempt(test_async_task.as_view()), name="api-test_task"),
]

# urlpatterns = [
#     path('orders/order_create/', OrderViewSet.as_view({'post': 'create'})),
#     path('orders/<int:pk>/order_delete/', OrderViewSet.as_view({'delete': 'order_delete'})),
# ]
#
#
urlpatterns += router.urls
