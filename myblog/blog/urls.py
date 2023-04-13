from django.urls import path, include
from rest_framework import routers
from . import views

router = routers.DefaultRouter()
router.register(r'api/post', views.PostViewSet, basename="post")
router.register(r'api/comment', views.CommentViewSet)

urlpatterns = [
    path('', views.index, name='index'),
    path('register/', views.register_request, name='register'),
    path('login/', views.login_request, name='login'),
    path('logout/', views.logout_request, name='logout'),
    path('api/post/my-tags/', views.PostViewSet.as_view({'get': 'my_tags'}), name='my-tags'),
    path('', include(router.urls)),
]


# urlpatterns=[
#   path('',views.index, name='index'),
#   path('register', views.register_request, name='register'),
#   path("login", views.login_request, name="login"),
#   path("logout", views.logout_request, name= "logout"),
#   path("api/post", views.PostViewSet.as_view({'get': 'list',
#                                               'post':'create'}),
#        name="api/post"),
#   path('api/post/<int:pk>/', views.PostViewSet.as_view({'get': 'retrieve',
#                                                         'patch': 'partial_update',
#                                                         'delete': 'destroy'}),
#        name='post_detail'),
#   path("api/comment", views.CommentViewSet.as_view({'get': 'list','post':'create'}),
#        name="comment-list"),
#   path('api/comment/<int:pk>/', views.CommentViewSet.as_view({'get': 'retrieve',
#                                                               'patch': 'partial_update',
#                                                               'delete': 'destroy'}),
#        name='comment-detail'),
# ]