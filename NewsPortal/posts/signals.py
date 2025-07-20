from django.db.models.signals import m2m_changed
from django.dispatch import receiver
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from .models import PostCategory
from django.conf import settings

@receiver(m2m_changed, sender=PostCategory)
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