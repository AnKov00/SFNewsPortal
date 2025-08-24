from django.urls import path, include
from .views import (PostList, PostSearch, OnePost, NewsCreate, NewsUpdate,
                    NewsDelete, make_author, CategoryList, subscribe_category,)
from django.views.decorators.cache import cache_page

urlpatterns = [
    path('news/', cache_page(60)(PostList.as_view()), name='post_list'),
    path('news/<int:pk>/',cache_page(60*5)(OnePost.as_view()), name='post_detail'),
    path('news/search/', PostSearch.as_view(), name='post_search'),
    path('news/create/', NewsCreate.as_view(), name='news_create'),
    path('articles/create/', NewsCreate.as_view(), name='articles_create'),
    path('news/<int:pk>/edit/', NewsUpdate.as_view(), name='edit_news'),
    path('articles/<int:pk>/edit/', NewsUpdate.as_view(), name='edit_articles'),
    path('news/<int:pk>/delete/', NewsDelete.as_view(), name='delete_news'),
    path('articles/<int:pk>/edit/', NewsDelete.as_view(), name='delete_articles'),
    path('iauthor/', make_author, name='makeauthor'),
    path('category/', CategoryList.as_view(), name='category'),
    path('subscribe/<int:category_id>/', subscribe_category, name='subscribe'),

]