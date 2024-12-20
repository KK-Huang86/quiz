from Urmart import views
from django.urls import path,include
from django.views.decorators.csrf import csrf_exempt
from .views import test_async_task

from rest_framework.urlpatterns import format_suffix_patterns

# urlpatterns = [
#     path('order_create', views.OrderViewSet.as_view({'post': 'order_create'})),
#     path('order_delete', views.OrderViewSet.as_view({'delete': 'order_delete'})),
# path('order_list', views.OrderViewSet.as_view({'get': 'order_list'})),]
# urlpatterns = format_suffix_patterns(urlpatterns)
from rest_framework.routers import DefaultRouter
from .views import OrderViewSet,MemberViewSet,ProductViewSet

router = DefaultRouter()

router.register(r'orders', OrderViewSet, basename='order')
router.register(r'members', MemberViewSet)
router.register(r'products', ProductViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('api/test_task',csrf_exempt(test_async_task.as_view()),name='api-test_task'),

]

# urlpatterns = [
#     path('orders/order_create/', OrderViewSet.as_view({'post': 'create'})),
#     path('orders/<int:pk>/order_delete/', OrderViewSet.as_view({'delete': 'order_delete'})),
# ]
#
#
# urlpatterns += router.urls