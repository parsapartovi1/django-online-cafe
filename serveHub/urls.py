from django.urls import path
from .views import DiscountList, CategoryList, DiscountDetailView
from . import views
from user.views import create_comment
# app_name = 'serveHub'

urlpatterns = [
    path("discount/", DiscountList.as_view(), name="discount-list"),
    path("discount/<int:pk>/", DiscountDetailView.as_view(), name="discount-detail"),
    path("category/", CategoryList.as_view(), name="category-list"),
    path("", views.home, name="home"),
    path("products/", views.ProductListView.as_view(), name="product_list"),


    path("add-to-cart/<int:product_id>/", views.add_to_cart, name="add_to_cart"),

    path("tables/reserve/", views.TableReservationView.as_view(), name="table_reservation"),
    path("tables/reserve/<int:table_id>/", views.ReserveTableView.as_view(), name="reserve_table"),
    path('reserve-table/<int:table_id>/', views.reserve_table, name='reserve_table'),
    path('product/<int:pk>/', views.ProductDetailView.as_view(), name='product_detail'),
    path('product/<int:product_id>/comment/', create_comment, name='create_comment'),
]