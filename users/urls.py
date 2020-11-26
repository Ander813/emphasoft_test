from django.urls import path
from . import api_views

urlpatterns = [
    path('users/', api_views.UsersListCreateView.as_view(), name='users_list_create'),
    path('users/<int:pk>/', api_views.UserDetailView.as_view(), name='user_detail')
]