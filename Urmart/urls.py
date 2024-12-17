from Urmart import views
from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns

urlpatterns = [
    path('order_create', views.OrderViewSet.as_view({'post': 'order_create'})),
    path('order_delete', views.OrderViewSet.as_view({'delete': 'order_delete'})),]
urlpatterns = format_suffix_patterns(urlpatterns)
