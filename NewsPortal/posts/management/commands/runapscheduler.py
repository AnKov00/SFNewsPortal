import logging

from django.conf import settings

from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.triggers.cron import CronTrigger
from django.core.management.base import BaseCommand
from django_apscheduler.jobstores import DjangoJobStore
from django_apscheduler.models import DjangoJobExecution
from django.contrib.auth.models import User
from ...models import Post
from datetime import timedelta
from django.utils import timezone

logger = logging.getLogger(__name__)


# наша задача по выводу текста на экран
def my_job():
    week_ago = timezone.now() - timedelta(days=7)
    weekly_posts = Post.objects.filter(time_create__gte=week_ago)
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


# функция, которая будет удалять неактуальные задачи
def delete_old_job_executions(max_age=604_800):
    """This job deletes all apscheduler job executions older than `max_age` from the database."""
    DjangoJobExecution.objects.delete_old_job_executions(max_age)


class Command(BaseCommand):
    help = "Runs apscheduler."

    def handle(self, *args, **options):
        scheduler = BlockingScheduler(timezone=settings.TIME_ZONE)
        scheduler.add_jobstore(DjangoJobStore(), "default")

        # добавляем работу нашему задачнику
        scheduler.add_job(
            my_job,
            trigger=CronTrigger(day_of_week="mon", hour=8, minute=0),
            # То же, что и интервал, но задача тригера таким образом более понятна django
            id="my_job",  # уникальный айди
            max_instances=1,
            replace_existing=True,
        )
        logger.info("Added job 'my_job'.")

        scheduler.add_job(
            delete_old_job_executions,
            trigger=CronTrigger(
                day_of_week="mon", hour="00", minute="00"
            ),
            # Каждую неделю будут удаляться старые задачи, которые либо не удалось выполнить, либо уже выполнять не надо.
            id="delete_old_job_executions",
            max_instances=1,
            replace_existing=True,
        )
        logger.info(
            "Added weekly job: 'delete_old_job_executions'."
        )

        try:
            logger.info("Starting scheduler...")
            scheduler.start()
        except KeyboardInterrupt:
            logger.info("Stopping scheduler...")
            scheduler.shutdown()
            logger.info("Scheduler shut down successfully!")