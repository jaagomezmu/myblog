from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class BlogPost(models.Model):
    title = models.CharField(blank = False, max_length = 100)
    body = models.CharField(blank = False, max_length = 250)
    author = models.ForeignKey(User, on_delete = models.CASCADE, null = False)

    def __str__(self):
        return self.title


class Comment(models.Model):
    body = models.CharField(blank = False, max_length = 255)
    blogpost = models.ForeignKey(BlogPost, on_delete=models.CASCADE, null=False)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    
    def __str__(self):
        return self.body