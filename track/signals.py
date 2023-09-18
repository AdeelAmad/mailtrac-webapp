from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.dispatch import receiver
from .models import tracker
import easypost
easypost.api_key = ""

@receiver(post_save, sender=tracker)
def create_tracker(sender, instance, created, *args ,**kwargs):
    print('success')
    if created:
        tracker = easypost.Tracker.create(
            tracking_code='EZ3000000004',
        )
