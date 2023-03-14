from ..models import BlogPost
from rest_framework import serializers


class BlogPostSerializer(serializers.ModelSerializer):
    class Meta:
        model = BlogPost
        fields = ('body', 'title', 'author')