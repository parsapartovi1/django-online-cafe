# urls.py
from django.urls import path
from .views import UserRegisterView, UserLoginView, UserProfileView, UserLogoutView, AddReply
from . import views
urlpatterns = [
    path('register/', UserRegisterView.as_view(), name='user_register'),
    path('login/', UserLoginView.as_view(), name='user_login'),
    path('profile/', UserProfileView.as_view(), name='user_profile'),
    path('logout/', UserLogoutView.as_view(), name='user_logout'),


    path('product/<int:product_id>/comment/', views.create_comment, name='create_comment'),


    path('comment/<int:comment_id>/add_reply/', AddReply.as_view(), name='add_reply'),

    path('working_shift/create/', views.create_working_shift, name='create_working_shift'),
    path('working_shift/list/', views.list_working_shifts, name='list_working_shifts'),
]
