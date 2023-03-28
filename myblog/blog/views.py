from blog.api.serializers import BlogPostSerializer, CommentSerializer, CommentCreateSerializer
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.http import HttpResponse
from django.shortcuts import redirect, render
from rest_framework.authentication import BasicAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet

from .forms import NewUserForm
from .models import BlogPost, Comment


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

class PostViewSet(ModelViewSet):
    
    queryset = BlogPost.objects.order_by('title').all()
    serializer_class = BlogPostSerializer
    
    authentication_classes = [BasicAuthentication]
    permission_classes = [IsAuthenticated]
        
    def perform_create(self, serializer):
        serializer.save(author = self.request.user)

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