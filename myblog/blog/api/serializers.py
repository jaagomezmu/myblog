from ..models import BlogPost
from rest_framework import serializers


class BlogPostSerializer(serializers.ModelSerializer):
    # Declare the new names to the serializer
    # This is necessary because my model does  not have the same names as the exercise requests.
    text = serializers.CharField(source = 'title')
    user = serializers.IntegerField(source = 'author.id')
    class Meta:
        model = BlogPost
        fields = ('body', 'text', 'user')