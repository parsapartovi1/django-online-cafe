from django.urls import path
from .views import OrderList, OrderDetailView

urlpatterns = [
    path("order/", OrderList.as_view(), name="order-list"),
    path("order/<int:pk>/", OrderDetailView.as_view(), name="order-detail"),
]
