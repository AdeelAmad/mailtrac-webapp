from django.db import models
import uuid
from django.contrib.auth.models import User
from django.urls import reverse

CARRIERS = [
    ('USPS', 'USPS'),
    ('FedEx', 'FedEx'),
    ('UPS', 'UPS'),
    ('Other', 'Other'),

]


# Create your models here.
class tracker(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    name = models.CharField(max_length=150)
    description = models.TextField(default=None)
    tracking_number = models.CharField(max_length=50)
    carrier = models.CharField(max_length=8, choices=CARRIERS)
    sms = models.BooleanField(default=False)

    def get_absolute_url(self):
        return reverse('answer-detail', kwargs={'pk': self.pk})

