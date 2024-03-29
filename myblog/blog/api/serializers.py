from ..models import BlogPost, Comment
from rest_framework import serializers

class BlogPostSerializer(serializers.ModelSerializer):
    author = serializers.StringRelatedField(many=False, read_only =True)
    tagged_users = serializers.StringRelatedField(many=True)
    
    class Meta:
        model = BlogPost
        fields = ('title', 'body', 'author', 'created_at', 'img', 'safe',
                  'tagged_users', 'tagged_count', 'last_tag_date')

class CommentSerializer(serializers.ModelSerializer):
    blogpost = serializers.SerializerMethodField()
    class Meta:
        model = Comment
        fields = ('body', 'blogpost', 'user', 'created_at')
    
    def get_blogpost(self, obj):
        post = obj.blogpost
        return {'title': post.title, 'id': post.id}

class CommentCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ('body', 'blogpost', 'user', 'created_at')
        read_only_fields = ('user',)

class BlogPostTitleSerializer(serializers.ModelSerializer):
    class Meta:
        model = BlogPost
        fields = ('id', 'title')