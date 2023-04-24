import django_filters.rest_framework as filters
from blog.api.serializers import (BlogPostSerializer, BlogPostTitleSerializer,
                                  CommentCreateSerializer, CommentSerializer)
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.contenttypes.models import ContentType
from django.db.models import Count, Max
from django.http import HttpResponse
from django.shortcuts import redirect, render
from rest_framework.authentication import BasicAuthentication
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from .forms import NewUserForm
from .models import BlogPost, Comment, Like


def index(request):
    return HttpResponse("This will be the blog index, work in progress")

def register_request(request):
    if request.method == "POST":
        form = NewUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Registration successful." )
            return redirect("index")
        messages.error(request, "Unsuccessful registration. Invalid information.")
    form = NewUserForm()
    return render (request=request, template_name="blog/register.html", context={"register_form":form})

def login_request(request):
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.info(request, f"You are now logged in as {username}.")
                return redirect("index")
            else:
                messages.error(request,"Invalid username or password.")
        else:
            messages.error(request,"Invalid username or password.")
    form = AuthenticationForm()
    return render(request=request, template_name="blog/login.html", context={"login_form":form})

def logout_request(request):
    logout(request)
    messages.info(request, "You have successfully logged out.") 
    return redirect("index")

class BlogPostFilter(filters.FilterSet):
    user = filters.CharFilter(field_name='author__username')
    safe = filters.BooleanFilter(field_name='safe')

    class Meta:
        model = BlogPost
        fields = ['user', 'safe']

class PostViewSet(ModelViewSet):
    
    queryset = BlogPost.objects.order_by('title').all()
    serializer_class = BlogPostSerializer
    
    authentication_classes = [BasicAuthentication]
    permission_classes = [IsAuthenticated]
    
    filterset_class = BlogPostFilter
    search_fields = ['title', 'body', 'author__username']
    ordering_fields = ['title', 'author__username']
        
    def perform_create(self, serializer):
        serializer.save(author = self.request.user)
    
    def get_queryset(self):
        if self.action == 'my_tags':
            return BlogPost.objects.filter(tagged_users=self.request.user)
        return super().get_queryset()
           
    def get_serializer_class(self):
        if self.action == 'my_tags':
            return BlogPostTitleSerializer
        return self.serializer_class
    
    @action(detail=False, methods=['get'], url_path="my-tags")
    def my_tags(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)
    
    @action(detail=True, methods=['post'], url_path='like')
    def like(self, request, pk=None):
        post = self.get_object()
        try:
            like = Like.objects.get(user=request.user, content_type=ContentType.objects.get_for_model(post), object_id=post.id)
            like.delete()
            return Response({'status': 'unliked'})
        except Like.DoesNotExist:
            Like.objects.create(user=request.user, content_object=post)
            return Response({'status': 'liked'})
    
    @action(detail=True, methods=['post'], url_path='unlike')
    def unlike(self, request, pk=None):
        post = self.get_object()
        try:
            like = Like.objects.get(user=request.user, content_type=ContentType.objects.get_for_model(post), object_id=post.id)
            like.delete()
            return Response({'status': 'unliked'})
        except Like.DoesNotExist:
            return Response({'status': 'not liked'})

class CommentViewSet(ModelViewSet):
    
    queryset = Comment.objects.order_by('blogpost').all()
    serializer_class = CommentSerializer
    
    authentication_classes = [BasicAuthentication]
    permission_classes = [IsAuthenticated]
        
    def perform_create(self, serializer):
        serializer.save(user = self.request.user)
    
    def get_serializer_class(self):
        if self.request.method == 'POST':
            return CommentCreateSerializer
        return CommentSerializer