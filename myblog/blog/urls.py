from django.urls import path
from . import views

urlpatterns=[
  path('',views.index, name='index'),
  path('register', views.register_request, name='register'),
  path("login", views.login_request, name="login"),
  path("logout", views.logout_request, name= "logout"),
  path("api/post", views.PostViewSet.as_view({'get': 'list','post':'create'}), name="api/post"),
  path('api/post/<int:pk>/', views.PostViewSet.as_view({'get': 'retrieve','patch': 'partial_update','delete': 'destroy'}), name='post_detail'),
]
