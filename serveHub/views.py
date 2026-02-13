from django.views.generic import ListView, DetailView
from .models import Discount, Category


class DiscountList(ListView):
    model = Discount
    template_name = "discount_list.html"


class DiscountDetailView(DetailView):
    model = Discount
    template_name = "discount_detail.html"


class CategoryList(ListView):
    model = Category
    template_name = "category_list.html"


class CategoryDetailView(DetailView):
    model = Category
    template_name = "category_detail.html"
