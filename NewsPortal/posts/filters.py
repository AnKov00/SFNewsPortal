from django.forms import DateInput
from django_filters import FilterSet, CharFilter, DateFilter

from .models import Post

class PostFilter(FilterSet):
    author__name = CharFilter (lookup_expr='icontains')
    time_create = DateFilter(
        field_name='time_create',
        lookup_expr='gte',
        widget=DateInput(attrs={'type': 'date'}))

    class Meta:
        model = Post
        fields = {'title' : ['icontains']}

