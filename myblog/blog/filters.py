from django_filters import rest_framework as filters
from .models import BlogPost, Comment

class BlogPostFilter(filters.FilterSet):
    created_at_after = filters.DateFilter(field_name='created_at', lookup_expr='gte')
    created_at_before = filters.DateFilter(field_name='created_at', lookup_expr='lte')
    user = filters.CharFilter(field_name='author__username')
    safe = filters.BooleanFilter(field_name='safe')

    class Meta:
        model = BlogPost
        fields = ['created_at_after', 'created_at_before', 'user','safe']

class CommentFilter(filters.FilterSet):
    created_at_after = filters.DateFilter(field_name='created_at', lookup_expr='gte')
    created_at_before = filters.DateFilter(field_name='created_at', lookup_expr='lte')

    class Meta:
        model = Comment
        fields = ['created_at_after', 'created_at_before']
