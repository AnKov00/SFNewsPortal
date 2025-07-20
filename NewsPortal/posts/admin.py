from django.contrib import admin
from .models import Post, Category, PostCategory

# admin.site.register(Post)
admin.site.register(Category)

class PostCategoryInline(admin.TabularInline):
    model = PostCategory
    extra = 1


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    fields = ['title', 'text_news', 'author', ]
    inlines = [PostCategoryInline]
    list_display = ('title', 'author', 'display_categories')
    def display_categories(self, obj):
        return ", ".join([cat.name for cat in obj.category.all()])
    display_categories.short_description = 'Категории'
