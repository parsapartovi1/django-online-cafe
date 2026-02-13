from django.views.generic import ListView, DetailView
from .models import Order


class OrderList(ListView):
    model = Order
    template_name = "order_list.html"


class OrderDetailView(DetailView):
    model = Order
    template_name = "order_detail.html"
