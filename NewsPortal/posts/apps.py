from django.apps import AppConfig


class PostsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'posts'
    def ready(self):
        print("PostsConfig ready() вызвано!")  # Для отладки
        import posts.signals

