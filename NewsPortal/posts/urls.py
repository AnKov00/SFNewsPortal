from django.urls import path
from .views import PostList, PostSearch, OnePost, NewsCreate, NewsUpdate, NewsDelete


urlpatterns = [
    path('news/', PostList.as_view(), name='post_list'),
    path('news/<int:pk>',OnePost.as_view(), name='post_detail'),
    path('news/search/', PostSearch.as_view(), name='post_search'),
    path('news/create/', NewsCreate.as_view(), name='news_create'),
    path('articles/create/', NewsCreate.as_view(), name='articles_create'),
    path('news/<int:pk>/edit/', NewsUpdate.as_view(), name='edit_news'),
    path('articles/<int:pk>/edit/', NewsUpdate.as_view(), name='edit_articles'),
    path('news/<int:pk>/delete/', NewsDelete.as_view(), name='delete_news'),
    path('articles/<int:pk>/edit/', NewsDelete.as_view(), name='delete_articles'),
]