from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.contrib.contenttypes.fields import GenericForeignKey, GenericRelation
from django.contrib.contenttypes.models import ContentType
from django.db.models import UniqueConstraint

class BlogPost(models.Model):
    title = models.CharField(blank = False, max_length = 100)
    body = models.CharField(blank = False, max_length = 250)
    author = models.ForeignKey(User, on_delete = models.CASCADE, null = False)
    created_at = models.DateTimeField(auto_now_add=True)
    img = models.ImageField(upload_to='uploads/%Y/%m/%d/', blank=True, null=True)
    safe = models.BooleanField(default=True)
    tagged_users = models.ManyToManyField(User, through='UserTag', related_name='tagged_posts')
    likes = GenericRelation('Like', related_query_name='posts')
    
    @property
    def comments_count(self):
        return Comment.objects.filter(blogpost=self).count()
    
    @property
    def tagged_count(self):
        return self.tagged_users.count()
    
    @property
    def last_tag_date(self):
        last_tag = self.usertags.order_by('-created_at').first()
        if last_tag:
            return last_tag.created_at
        else:
            return None

    def __str__(self):
        return self.title


class Comment(models.Model):
    body = models.CharField(blank = False, max_length = 255)
    blogpost = models.ForeignKey(BlogPost, on_delete=models.CASCADE, null=False)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    likes = GenericRelation('Like', related_query_name='comments')
    
    def __str__(self):
        return self.body

class UserTag(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    blogpost = models.ForeignKey(BlogPost, on_delete=models.CASCADE, related_name='usertags')
    created_at = models.DateTimeField(auto_now_add=True)

class Like(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(default=timezone.now)
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')

    class Meta:
        constraints = [
            UniqueConstraint(fields=['user', 'content_type', 'object_id'], name='unique_like')
        ]
    