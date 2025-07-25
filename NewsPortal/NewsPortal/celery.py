import os
from celery import Celery
from celery.schedules import crontab


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'NewsPortal.settings')
app = Celery('NewsPortal')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()

app.conf.beat_schedule = {
    'newsletter_every_monday_at_8':{
        'task':'posts.task.weekly_newsletter',
        'schedule':crontab(hour=8,minute=0, day_of_week=1),
        }
}
