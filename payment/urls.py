from django.urls import path

from .views import OrderList, OrderDetailView

urlpatterns = [
    path("order/", OrderList.as_view(), name="order-list"),
    path("order/<int:pk>/", OrderDetailView.as_view(), name="order-detail"),

from . import views

urlpatterns = [
    path('pay/create/', views.create_payment, name='create_payment'),
    path('pay/list/', views.list_payments, name='list_payments'),

]
