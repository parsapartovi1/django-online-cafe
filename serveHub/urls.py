from django.urls import path
from . import views

app_name = 'serveHub'

urlpatterns = [
    path('', views.home, name='home'),
    path('products/', views.ProductListView.as_view(), name='product_list'),
    path('products/new/', views.ProductCreateView.as_view(), name='product_create'),
    path('products/<int:pk>/edit/', views.ProductUpdateView.as_view(), name='product_update'),
    path('products/<int:pk>/delete/', views.ProductDeleteView.as_view(), name='product_delete'),
    path('tables/', views.TableListView.as_view(), name='table_list'),
    path('tables/new/', views.TableCreateView.as_view(), name='table_create'),
    path('tables/<int:pk>/edit/', views.TableUpdateView.as_view(), name='table_update'),
]