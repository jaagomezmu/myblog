from ..models import BlogPost
from rest_framework import serializers


class BlogPostSerializer(serializers.ModelSerializer):
    author = serializers.StringRelatedField(many=False, read_only =True)
    
    class Meta:
        model = BlogPost
        fields = ('body', 'title', 'author')