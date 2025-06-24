from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView,UpdateView, DeleteView
from .models import Post
from .filters import PostFilter
from .forms import PostForm

class PostList(ListView):
    model = Post
    ordering = '-time_create'
    template_name = 'news_list.html'
    context_object_name = 'news'
    paginate_by = 10


class PostSearch(ListView):
    model = Post
    ordering = 'title'
    template_name = 'search_list.html'
    context_object_name = 'news'
    paginate_by = 5

    def get_queryset(self):
        queryset = super().get_queryset()
        self.filterset = PostFilter(self.request.GET, queryset)
        return self.filterset.qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filterset'] = self.filterset
        return context


class OnePost(DetailView):
    model = Post
    template_name = 'one_post.html'
    context_object_name = 'post'


class NewsCreate(CreateView):
    form_class = PostForm
    model = Post
    template_name = 'create_post.html'

    def form_valid(self, form):
        post = form.save(commit=False)
        post.type = 'nw'
        return super().form_valid(form)


class ArticCreate(CreateView):
    form_class = PostForm
    model = Post
    template_name = 'create_post.html'

    def form_valid(self, form):
        post = form.save(commit=False)
        post.type = 'st'
        return super().form_valid(form)


class NewsUpdate(UpdateView):
    form_class = PostForm
    model = Post
    template_name = 'create_post.html'

class NewsDelete(DeleteView):
    model = Post
    template_name = 'post_delete.html'
    success_url = reverse_lazy('post_list')