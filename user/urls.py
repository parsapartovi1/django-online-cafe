# urls.py
from django.urls import path
from .views import UserRegisterView, UserLoginView, UserProfileView, UserLogoutView, AddReply

urlpatterns = [
    path('register/', UserRegisterView.as_view(), name='user_register'),
    path('login/', UserLoginView.as_view(), name='user_login'),
    path('profile/', UserProfileView.as_view(), name='user_profile'),
    path('logout/', UserLogoutView.as_view(), name='user_logout'),
    path('comment/<int:comment_id>/add_reply/', AddReply.as_view(), name='add_reply'), 
]
