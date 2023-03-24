from django.urls import path
from . import views

urlpatterns=[
  path('',views.index, name='index'),
  path('register', views.register_request, name='register'),
  path("login", views.login_request, name="login"),
  path("logout", views.logout_request, name= "logout"),
  path("api/post", views.PostsViewSet.as_view(), name="api/post"),
  path('api/post/<int:pk>/', views.PostDetailViewSet.as_view(), name='post_detail'),
]
