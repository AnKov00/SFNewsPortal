from django.core.management.base import BaseCommand
from posts.models import Post, Category

class Command(BaseCommand):
    help = 'Удаляет все новости по выбранной категории'
    def add_arguments(self, parser):
        parser.add_argument('id', type=int, help='ID категории')

    def handle(self, *args, **options):
        self.stdout.readable()
        self.stdout.write(f'Уверены, что хотите удалить все новости из категории {Category.objects.get(pk=options['id']).name}? yes/no')
        answer = input()
        if answer == 'yes':
            try:
                Post.objects.filter(post_categories__category_id=options['id']).delete()
                self.stdout.write(self.style.SUCCESS('Новости удалены'))
                return
            except Exception as e:
                self.stdout.write(f'Ошибка {e}')
        self.stdout.write('Ошибка доступа')
