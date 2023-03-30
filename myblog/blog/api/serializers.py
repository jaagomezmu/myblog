from ..models import BlogPost, Comment
from rest_framework import serializers


class BlogPostSerializer(serializers.ModelSerializer):
    author = serializers.StringRelatedField(many=False, read_only =True)
    
    class Meta:
        model = BlogPost
        fields = '__all__'

class CommentSerializer(serializers.ModelSerializer):
    blogpost = serializers.SerializerMethodField()
    class Meta:
        model = Comment
        fields = '__all__'
    
    def get_blogpost(self, obj):
        post = obj.blogpost
        return {'title': post.title, 'id': post.id}

class CommentCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = '__all__'
        read_only_fields = ('user',)
