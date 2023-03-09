from ..models import BlogPost
from rest_framework import serializers


class BlogPostSerializer(serializers.Serializer):
    body = serializers.CharField()
    text = serializers.CharField(source = 'title')
    user = serializers.IntegerField(source = 'author.id')