from django.shortcuts import render
from django.views.generic import ListView, DetailView
from .models import Post

class PostList(ListView):
    model = Post
    ordering = '-time_create'
    template_name = 'news_list.html'
    context_object_name = 'news'


class OnePost(DetailView):
    model = Post
    template_name = 'one_post.html'
    context_object_name = 'post'

# Create your views here.
