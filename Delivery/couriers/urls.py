from django.urls import path
from couriers import views

urlpatterns = [
    path('couriers', views.create_couriers),
    path('couriers/<int:courier_id>', views.get_courier),
]
