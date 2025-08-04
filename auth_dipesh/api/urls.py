from django.urls import path
from auth_dipesh.api.views import UserListCreateAPIView, UserDetailAPIView, UserLoginAPIView, SayHelloAPIView


urlpatterns = [
    path("users/", UserListCreateAPIView.as_view(), name='user-list-create'),
    path("users/<int:pk>", UserDetailAPIView.as_view(), name='user-detail'),
    path("login/", UserLoginAPIView.as_view(), name='user-login'),

    path("check/", SayHelloAPIView.as_view(), name='check-view'),
]