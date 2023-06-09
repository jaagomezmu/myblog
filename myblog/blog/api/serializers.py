import redis
from ..models import BlogPost, Comment
from rest_framework import serializers

redis_connection = redis.Redis(host='localhost', port=6379, db=0)

class BlogPostSerializer(serializers.ModelSerializer):
    author = serializers.StringRelatedField(many=False, read_only =True)
    tagged_users = serializers.StringRelatedField(many=True)
    visits_count = serializers.SerializerMethodField()
    
    class Meta:
        model = BlogPost
        fields = ('title', 'body', 'author', 'created_at', 'img', 'safe',
                  'tagged_users', 'tagged_count', 'last_tag_date', 'visits_count')
    
    def get_visits_count(self, obj):
        pk = obj.pk
        key = f'post:{pk}:visits'
        visits = redis_connection.get(key)
        if visits is not None:
            return int(visits)
        return 0

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