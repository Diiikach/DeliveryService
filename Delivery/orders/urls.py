from django.urls import path
from orders import views

urlpatterns = [
    path('orders', views.create_orders),
    path('orders/assign', views.assign_orders),
    path('orders/complete', views.complete_order),
]
