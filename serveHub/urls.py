from django.urls import path
from .views import DiscountList, CategoryList, DiscountDetailView, CategoryDetailView


urlpatterns = [
    path("discount/", DiscountList.as_view(), name="discount-list"),
    path("discount/<int:pk>/", DiscountDetailView.as_view(), name="discount-detail"),
    path("category/", CategoryList.as_view(), name="category-list"),
    path("category/<int:pk>/", CategoryDetailView.as_view(), name="category-detail"),
]
