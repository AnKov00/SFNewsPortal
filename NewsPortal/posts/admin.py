from django.contrib import admin
from django.contrib.auth.models import User

from .models import Post, Category, PostCategory

def nullfy_rating(modeladmin, request, queryset):
    queryset.update(rating_news=0)

nullfy_rating.short_description = 'Обнулить рейтинг статьи'

admin.site.register(Category)

class PostCategoryInline(admin.TabularInline):
    model = PostCategory
    extra = 1


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    fields = ['title', 'text_news', 'author', 'rating_news']
    inlines = [PostCategoryInline]
    list_display = ('title', 'author', 'display_categories', 'rating_news')
    def display_categories(self, obj):
        return ", ".join([cat.name for cat in obj.category.all()])
    display_categories.short_description = 'Категории'
    list_filter = ('category__name', 'author__name' )
    search_fields = ('text_news', )
    actions = [nullfy_rating]

admin.site.unregister(User)