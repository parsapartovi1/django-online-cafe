from django.urls import path
from . import views

urlpatterns = [
    path('pay/create/', views.create_payment, name='create_payment'),
    path('pay/list/', views.list_payments, name='list_payments'),
]
