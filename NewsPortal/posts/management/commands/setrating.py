from django.core.management.base import BaseCommand
from posts.models import Post

class Command(BaseCommand):
    help = 'Устанавливает рейтинг для статьи по id'

    def add_arguments(self, parser):
        parser.add_argument('id', type=int, help='ID статьи')
        parser.add_argument('--rating', type=int, help='Новый рейтинг')

    def handle(self, *args, **options):
        try:
            post = Post.objects.get(pk=options['id'])
            post.rating_news = options['rating']
            post.save()
            self.stdout.write(self.style.SUCCESS(
                f'Рейтинг статьи "{post.title}" обновлен, теперь он равен {options["rating"]}'
            ))
        except Post.DoesNotExist:
            self.stderr.write(self.style.ERROR(
                f'Новости с id={options["id"]} не существует'
            ))