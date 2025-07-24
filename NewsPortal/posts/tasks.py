from celery import shared_task
from django.contrib.auth.models import User
from django.template.loader import render_to_string
from django.core.mail import EmailMultiAlternatives
from django.conf import settings
from django.utils import timezone
from datetime import timedelta
from .models import Post



@shared_task
def weekly_newsletter():
    week_ago = timezone.now() - timedelta(days=7)# день, который был неделю назад
    weekly_posts = Post.objects.filter(time_create__gt=week_ago) # Список объектов Post созданных за неделю
    send_data = {}
    for post in weekly_posts:
        categories = post.category.all() #находим все категории поста
        for category in categories:
            subscribers = category.subscribers.all() #находим всех подписчиков категории
            for user in subscribers:
                if user.email not in send_data:
                    send_data[user.email]=[post]
                else:
                    send_data[user.email].append(post)

    for email, posts in send_data.items():
        user = User.objects.get(email=email)
        html_content = render_to_string(
            'mail_template/weekly_post.html',
            {
                'user':user,
                'posts': posts,
            })
        msg = EmailMultiAlternatives(
            subject=f'Еженедельный дайджест новостей',
            body='',
            from_email=settings.EMAIL_HOST_USER,
            to=[email],)
        msg.attach_alternative(html_content, "text/html")
        msg.send()

@shared_task
def send_post_notifications(sender, instance, action, **kwargs):
    print('Отправка уведомления')
    if action == "post_add":
        print("m2m_change сигнал сработал")
        subscribers_data = {} # почта:категории
        # Перебираем все категории поста
        for post_category in instance.post_categories.all():
            category = post_category.category  # сама категория
            print(f'Обрабатываем категорию: {category.name}')
            for subscriber in category.subscribers.all():
                if not subscriber.email:
                    continue
                if subscriber.email not in subscribers_data:
                    subscribers_data[subscriber.email]={
                        'user': subscriber,
                        'categories':set()
                    }
                subscribers_data[subscriber.email]['categories'].add(category.name)
        for email, data in subscribers_data.items():
            user = data['user']
            categories = sorted(data['categories'])

            if len(categories) == 1:
                categories_text = f'Новая статья в вашей любимой категории {categories[0]}'
            else:
                categories_text = f'Новая статья в ваших любимых категориях: {', '.join(categories)}'
                context = {
                    'post': instance,
                    'username': user.username,
                    'category': categories_text,
                }
            html_content = render_to_string('mail_template/post_create.html', context)
            text_content = f"""
                            Здравствуйте, {user.username}!
                            Новая статья в {categories_text}: {instance.title}
                            Краткое содержание: {instance.text_news[:50]}...
                            Ссылка: http://127.0.0.1:8000/news/{instance.id}
                            """
            msg = EmailMultiAlternatives(
                subject=f'Новый пост: {instance.title}',
                from_email= settings.EMAIL_HOST_USER,
                to=[email]
            )
            msg.attach_alternative(html_content, 'text/html')
            msg.send()
            print(f"Отправлено письмо для {email} по категориям: {categories_text}")