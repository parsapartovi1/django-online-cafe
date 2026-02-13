from django.urls import path
from .views import DiscountList, CategoryList, DiscountDetailView, CategoryDetailView
from . import views

# app_name = 'serveHub'

urlpatterns = [
    path("discount/", DiscountList.as_view(), name="discount-list"),
    path("discount/<int:pk>/", DiscountDetailView.as_view(), name="discount-detail"),
    path("category/", CategoryList.as_view(), name="category-list"),
    path("category/<int:pk>/", CategoryDetailView.as_view(), name="category-detail"),
    path("", views.home, name="home"),
    path("products/", views.ProductListView.as_view(), name="product_list"),
    path("products/new/", views.ProductCreateView.as_view(), name="product_create"),
    path(
        "products/<int:id>/edit/",
        views.ProductUpdateView.as_view(),
        name="product_update",
    ),
    path(
        "products/<int:id>/delete/",
        views.ProductDeleteView.as_view(),
        name="product_delete",
    ),
    path("tables/", views.TableListView.as_view(), name="table_list"),
    path("tables/new/", views.TableCreateView.as_view(), name="table_create"),
    path("tables/<int:id>/edit/", views.TableUpdateView.as_view(), name="table_update"),
]
