# urls.py
from django.urls import path
from .views import ChangePasswordView, UserRegisterView, UserLoginView, UserProfileView, UserLogoutView, AddReply
from . import views

urlpatterns = [
    path('register/', UserRegisterView.as_view(), name='user_register'),
    path('login/', UserLoginView.as_view(), name='user_login'),
    path('profile/', UserProfileView.as_view(), name='user_profile'),
    path('logout/', UserLogoutView.as_view(), name='user_logout'),

    path('product-comments/', views.product_comments, name='product_comments'),
    path('comments/all/', views.admin_comment_list, name='admin_comment_list'),



    path('user/<int:comment_id>/add_reply/', AddReply.as_view(), name='add_reply'),
    path('reply/<int:reply_id>/delete/', views.delete_reply, name='delete_reply'),

    path('create_working_shift', views.create_working_shift, name='create_working_shift'),
    path('working_shift/list/', views.list_working_shifts, name='list_working_shifts'),

    path('change-password/', ChangePasswordView.as_view(), name='change_password'),


    path('music/', views.music_page, name='music_page'),

]
