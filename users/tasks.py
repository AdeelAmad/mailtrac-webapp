import os
import django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "mailtrac.settings")
django.setup()
from django.contrib.auth.models import User
from celery import shared_task
#
# @shared_task
# def monthly_tracks():
#
#     for user in User.objects.all():
#         profile_topoff(user)
#         return