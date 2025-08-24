from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import Post, Category, UsersCategory
from .filters import PostFilter
from .forms import PostForm
from django.shortcuts import redirect, get_object_or_404
from django.contrib.auth.models import Group
from django.contrib.auth.decorators import login_required
from django.core.cache import cache



class PostList(ListView):
    model = Post
    ordering = '-time_create'
    template_name = 'news_list.html'
    context_object_name = 'news'
    paginate_by = 10

class CategoryList(ListView):
    model = Category
    ordering = ['name']
    template_name = 'category_list.html'
    context_object_name = 'category'


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

    def get_object(self, *args, **kwargs):
        obj = cache.get(f'post-{self.kwargs["pk"]}', None)
        if not obj:
            obj = super().get_object(queryset=self.queryset)
            cache.set(f'post-{self.kwargs["pk"]}', obj)
        return obj


class NewsCreate(PermissionRequiredMixin, CreateView):
    permission_required = ('posts.add_post')
    form_class = PostForm
    model = Post
    template_name = 'create_post.html'


    def form_valid(self, form):
        post = form.save(commit=False)
        if '/news' in self.request.path:
            post.type = 'nw'
        elif '/articles' in self.request.path:
            post.type = 'st'
        post.save()
        form.save_m2m()
        return super().form_valid(form)


class NewsUpdate(PermissionRequiredMixin, UpdateView):
    permission_required = ('posts.change_post')
    form_class = PostForm
    model = Post
    template_name = 'create_post.html'
    success_url = reverse_lazy('post_list')

class NewsDelete(LoginRequiredMixin, DeleteView):
    model = Post
    template_name = 'post_delete.html'
    success_url = reverse_lazy('post_list')



@login_required
def make_author(request):
    user = request.user
    author_group = Group.objects.get(name='authors')


    if not user.groups.filter(name='authors').exists():
        author_group.user_set.add(user)

    return redirect('/news/')

@login_required
def subscribe_category(request, category_id):
    category = get_object_or_404(Category, id=category_id)
    user = request.user
    subscription, created = UsersCategory.objects.get_or_create(
        user=user,
        category=category
    )
    if not created:
        subscription.delete()
    return redirect('category')
