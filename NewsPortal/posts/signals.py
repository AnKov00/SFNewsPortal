from django.db.models.signals import m2m_changed
from django.dispatch import receiver
from .tasks import send_post_notifications
from .models import PostCategory


@receiver(m2m_changed, sender=PostCategory)
def post_created(sender, instance, action, **kwargs):
    if action == 'post_add':
        send_post_notifications.delay(sender, instance, action, **kwargs)